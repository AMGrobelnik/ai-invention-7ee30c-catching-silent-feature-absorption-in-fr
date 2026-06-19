#!/usr/bin/env python3
"""PART 1 of M7 (iter-5) — SECOND is-a hierarchy: bias_in_bios PROFESSIONS.

The NEW science of this experiment: does SAE feature absorption (a *general* parent
latent that is SUPPRESSED on specific children, with a mutually-exclusive specialist filling
the recall hole) generalise from the homograph-polysemy taxonomic case (Georgia) to a clean
is-a hierarchy = occupations? bias_in_bios rows are CORPUS-ONLY (no content pairs, no target
spans), so this is a corpus adaptation of the iter-4 two-track machinery:

  parent  = a general 'occupation/biography' latent (fires on most bios, precision-gated vs a
            non-bio negative pool of movie + restaurant reviews — same corpus file),
  child   = each of the 28 professions (the sub-contexts),
  hole    = a profession where the parent's recall collapses,
  absorber= a mutually-exclusive specialist (firing-Jaccard < 0.10) that fills the hole.

The EXPECTED, fully publishable outcome is the boundary-null: a *uniform-high* parent recall
across professions (NO holes) => 'absorption does not generalise to the profession is-a
hierarchy'. A qualifying profession with set_cover_established would be a positive SECOND case.

Reuses engine.py verbatim where possible (run_greedy, fast_auc, _auc_rows, bootstrap_ci,
paired_diff_ci, firing_jaccard_pos, match_threshold, _youden_table, holm, JumpReLU SAE loader).
Adds: a WHOLE-TEXT encoder (mean residual / max latent over all non-special tokens), corpus-only
parent identification, the per-profession hole table (all 28), and a per-profession set-cover +
selection-isolation block (run on qualifying professions; otherwise on the largest-hole profession
as a clearly-labelled DESCRIPTIVE best-case so the baseline comparison is never empty).
"""
from __future__ import annotations

import gc
import io
import json
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from loguru import logger

import engine as eng  # importing runs engine's hardware/logging setup (CUDA probe, RLIMIT, logger)
import torch

# ---- reuse engine constants verbatim ----
D_MODEL = eng.D_MODEL
SEED = eng.SEED
GREEDY_MAX_MEMBERS = eng.GREEDY_MAX_MEMBERS
G1_RECALL = eng.G1_RECALL
JACCARD_MAX = eng.JACCARD_MAX
SUBCTX_PREC = eng.SUBCTX_PREC
GAIN_MIN = eng.GAIN_MIN
PRECISION_FLOOR = eng.PRECISION_FLOOR
N_MIN_ELIGIBLE = eng.N_MIN_ELIGIBLE
DEVICE = eng.DEVICE
CACHE_DIR = eng.CACHE_DIR
RESULTS_DIR = eng.RESULTS_DIR

MAXLEN_BIOS = 256           # bio char_len up to ~500 => ~150 tok; covers it (+BOS)
BATCH = 16
CAP_PER_PROFESSION = 500    # bound GPU cost; >=300 keeps every profession >=150 in the held-out fold
N_NEG_TARGET = 5000         # non-bio negatives (movie + restaurant reviews), held-fixed pool size
FIRING_FLOOR = 0.05         # held-out anchor must fire on >5% of bios (the iter-4 letter-I fix)
NEG_CAP_SETCOVER = 2500     # cap one-vs-rest held-out negatives for the B=10k AUC bootstrap (cost)

BIOS_FAMILY = "bias_in_bios_boundary"
NEG_FAMILIES = ("sentiment", "restaurant_aspect")


# ============================================================================= data loading
def load_professions_and_negatives(data_path: Path, cap: int = CAP_PER_PROFESSION,
                                   n_neg: int = N_NEG_TARGET, seed: int = SEED) -> tuple:
    """Load bias_in_bios bios (capped per profession, stratified by gender) + a non-bio negative
    pool (movie + restaurant reviews) from the SAME corpus file, with identical whole-text pooling
    so the negative pool size is held fixed (no length confound)."""
    rng = np.random.default_rng(seed)
    logger.info(f"loading professions + negatives from {data_path}")
    blob = json.loads(Path(data_path).read_text())
    fam_rows: dict[str, list] = {}
    for ds in blob["datasets"]:
        for r in ds["examples"]:
            fam = r.get("metadata_family")
            fam_rows.setdefault(fam, []).append(r)
    del blob
    gc.collect()

    bios_all = fam_rows.get(BIOS_FAMILY, [])
    logger.info(f"  bias_in_bios rows available: {len(bios_all)}")
    # group by (profession, gender) -> capped stratified subsample
    by_pg: dict[tuple, list] = {}
    for r in bios_all:
        prof = r["output"]
        gender = (r.get("metadata_sub_context") or {}).get("gender", "unknown")
        by_pg.setdefault((prof, gender), []).append(r)
    professions = sorted({p for (p, _g) in by_pg})
    bios: list[dict] = []
    for prof in professions:
        for gender in ("male", "female", "unknown"):
            grp = by_pg.get((prof, gender), [])
            if not grp:
                continue
            # cap is per-profession; split across present genders proportionally
            n_present_genders = sum(1 for g in ("male", "female", "unknown") if by_pg.get((prof, g)))
            keep = min(len(grp), max(1, cap // max(1, n_present_genders)))
            idx = rng.permutation(len(grp))[:keep]
            bios.extend(grp[i] for i in idx)
    rng.shuffle(bios)
    for i, r in enumerate(bios):
        r["_row_id"] = i
        r["_profession"] = r["output"]
        r["_gender"] = (r.get("metadata_sub_context") or {}).get("gender", "unknown")
    logger.info(f"  bios kept (cap={cap}/prof): {len(bios)} across {len(professions)} professions")

    # negatives: stratified ~equal from each negative family, full texts
    neg: list[dict] = []
    per_fam = max(1, n_neg // len(NEG_FAMILIES))
    for fam in NEG_FAMILIES:
        grp = fam_rows.get(fam, [])
        idx = rng.permutation(len(grp))[:min(len(grp), per_fam)]
        for j in idx:
            neg.append(grp[j])
    rng.shuffle(neg)
    for i, r in enumerate(neg):
        r["_row_id"] = i
    logger.info(f"  negatives kept (non-bio reviews): {len(neg)} "
                f"({[ (fam, sum(1 for r in neg if r.get('metadata_family')==fam)) for fam in NEG_FAMILIES ]})")
    return bios, neg, professions


# ============================================================================= whole-text encoder
def _wholetext_positions(offsets, attn_mask) -> list[int]:
    """All real content tokens: attention_mask==1 AND non-zero-width char offset (drops BOS/pad,
    which carry a (0,0) offset)."""
    off = offsets.tolist() if hasattr(offsets, "tolist") else offsets
    L = len(off)
    if attn_mask is not None:
        am = attn_mask.tolist() if hasattr(attn_mask, "tolist") else attn_mask
    else:
        am = [1] * L
    return [t for t in range(L) if am[t] == 1 and off[t][1] > off[t][0]]


def determine_layer_idx_wholetext(model, tok, sae, rows: list[dict]) -> int:
    """Pick the HF hidden_states index whose residual the SAE reconstructs best (lowest PER-TOKEN
    FVU). blocks.12.hook_resid_post == hidden_states[13]; validate empirically. NOTE: FVU is
    computed per-token (the SAE is trained on per-token residuals); mean-pooling over ~80 bio
    tokens before reconstruction would inflate FVU as a pooling artifact, so we reconstruct each
    selected token and aggregate the error/variance across all tokens (matches encode_rows' FVU)."""
    sample = rows[:32]
    texts = [r["input"] for r in sample]
    enc = tok(texts, return_offsets_mapping=True, add_special_tokens=True, padding=True,
              truncation=True, max_length=MAXLEN_BIOS, return_tensors="pt")
    offsets = enc.pop("offset_mapping")
    enc = {k: v.to(DEVICE) for k, v in enc.items()}
    caps: dict = {}
    handles = []
    candidates = (11, 12, 13)
    for hi in candidates:
        def mk(h):
            def hook(_m, _i, out):
                caps[h] = out[0] if isinstance(out, tuple) else out
            return hook
        handles.append(model.model.layers[hi - 1].register_forward_hook(mk(hi)))
    with torch.no_grad():
        model.model(**enc)
    for h in handles:
        h.remove()
    results = {}
    for idx in candidates:
        hs = caps[idx]
        toks = []
        for i in range(len(sample)):
            pos = _wholetext_positions(offsets[i], enc["attention_mask"][i])
            if pos:
                toks.append(hs[i, pos].float())   # [npos, 2304] per token
        X = torch.cat(toks, 0)                    # [M, 2304] all selected tokens
        with torch.no_grad():
            recon = sae.decode(sae.encode(X.to(sae.W_dec.dtype))).float()
        sse = ((X - recon) ** 2).sum().item()
        sst = ((X - X.mean(0)) ** 2).sum().item()
        results[idx] = sse / max(sst, 1e-9)
    logger.info(f"  whole-text PER-TOKEN FVU by hidden_states idx: "
                f"{{12:{results[12]:.3f}, 13:{results[13]:.3f}, 11:{results[11]:.3f}}}")
    best = min(results, key=results.get)
    logger.info(f"  selected hidden_states[{best}] (HF decoder layer {best-1}); FVU={results[best]:.3f}")
    return best


class WholeTextEncoder:
    """Encode texts -> (CSR max-pooled latents [N,width], fp16 mean-pooled residual [N,2304]).
    Mirrors engine.Encoder but pools over ALL non-special tokens (no target span)."""

    def __init__(self, model, tok, sae, layer_idx: int):
        self.model, self.tok, self.sae = model, tok, sae
        self.layer_idx = layer_idx
        self.width = sae.W_dec.shape[0]
        self.sae_dtype = sae.W_dec.dtype
        self._cap: dict = {}

        def _hook(_mod, _inp, out):
            self._cap["resid"] = out[0] if isinstance(out, tuple) else out

        self._handle = model.model.layers[layer_idx - 1].register_forward_hook(_hook)

    def encode_rows(self, rows: list[dict]):
        N = len(rows)
        row_nz: dict[int, tuple] = {}
        resid = np.zeros((N, D_MODEL), dtype=np.float16)
        l0_sum = l0_cnt = 0.0
        fvu_sse = 0.0
        fvu_s1 = np.zeros(D_MODEL, dtype=np.float64)
        fvu_s2 = 0.0
        fvu_n = 0
        dropped = 0
        t0 = time.time()
        for b0 in range(0, N, BATCH):
            batch = rows[b0:b0 + BATCH]
            texts = [r["input"] for r in batch]
            enc = self.tok(texts, return_offsets_mapping=True, add_special_tokens=True,
                           padding=True, truncation=True, max_length=MAXLEN_BIOS, return_tensors="pt")
            offsets = enc.pop("offset_mapping")
            enc = {k: v.to(DEVICE) for k, v in enc.items()}
            with torch.no_grad():
                self.model.model(**enc)
                hs = self._cap["resid"]
            row_vecs, keep_rows = [], []
            for i in range(len(batch)):
                gid = b0 + i
                pos = _wholetext_positions(offsets[i], enc["attention_mask"][i])
                if not pos:
                    dropped += 1
                    continue
                keep_rows.append((gid, len(pos)))
                row_vecs.append(hs[i, pos].float())
            if not row_vecs:
                self._cap.clear()
                continue
            allres = torch.cat(row_vecs, 0)
            with torch.no_grad():
                lat = self.sae.encode(allres.to(self.sae_dtype)).float()
                recon = self.sae.decode(lat.to(self.sae_dtype)).float()
            err2 = ((allres - recon) ** 2).sum(1)
            m0 = 0
            for (gid, npos) in keep_rows:
                sl = lat[m0:m0 + npos]
                sr = allres[m0:m0 + npos]
                pooled_lat = sl.max(0).values
                resid[gid] = sr.mean(0).half().cpu().numpy()
                nz = torch.nonzero(pooled_lat > 0).squeeze(-1)
                row_nz[gid] = (nz.cpu().numpy().astype(np.int32),
                               pooled_lat[nz].cpu().numpy().astype(np.float32))
                l0_sum += float((sl > 0).sum().item())
                l0_cnt += npos
                fvu_sse += float(err2[m0:m0 + npos].sum().item())
                xv = sr.double()
                fvu_s1 += xv.sum(0).cpu().numpy()
                fvu_s2 += float((xv ** 2).sum().item())
                fvu_n += npos
                m0 += npos
            self._cap.clear()
            del hs, lat, recon, allres, err2
            if (b0 // BATCH) % 50 == 0:
                logger.info(f"    encoded {b0+len(batch)}/{N} ({(time.time()-t0):.0f}s)")
        lat_ptr = np.zeros(N + 1, dtype=np.int64)
        for gid in range(N):
            lat_ptr[gid + 1] = lat_ptr[gid] + (len(row_nz[gid][0]) if gid in row_nz else 0)
        total = int(lat_ptr[-1])
        lat_idx = np.zeros(total, dtype=np.int32)
        lat_data = np.zeros(total, dtype=np.float32)
        for gid in range(N):
            if gid in row_nz:
                a, b = lat_ptr[gid], lat_ptr[gid + 1]
                lat_idx[a:b], lat_data[a:b] = row_nz[gid]
        lat_csr = sp.csr_matrix((lat_data, lat_idx, lat_ptr), shape=(N, self.width))
        fvu = float("nan")
        if fvu_n > 0:
            sst = fvu_s2 - float(fvu_s1 @ fvu_s1) / fvu_n
            fvu = fvu_sse / max(sst, 1e-9)
        mean_l0 = l0_sum / max(l0_cnt, 1)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info(f"  encoded {N} rows in {time.time()-t0:.0f}s | dropped(no-pos)={dropped} "
                    f"| FVU={fvu:.3f} | meanL0={mean_l0:.1f} | nnz/row={lat_csr.nnz/max(N,1):.0f}")
        return lat_csr, resid, fvu, mean_l0, dropped


# ----- split-aware cache I/O: keep every cached blob <100MB for GitHub deployment -----
# Some whole-text encodings (e.g. the 13.8k-bio sparse latents) exceed 100MB even deflate-
# compressed (sp.save_npz already compresses, so gzip does NOT help). We therefore byte-chunk any
# cache file over the limit into `<name>.partNNN` pieces and reassemble transparently on load.
PART_BYTES = 90 * 1024 * 1024        # 90MB chunks (comfortably < 100MB)
SPLIT_THRESHOLD = 95 * 1024 * 1024   # split files larger than this on save


def _part_paths(path: Path) -> list[Path]:
    return sorted(path.parent.glob(f"{path.name}.part*"))


def _save_blob_split(path: Path):
    """If `path` exceeds the size threshold, byte-split it into `<name>.partNNN` and delete the
    original; otherwise leave it as a single file. Always clears any stale parts first."""
    for p in _part_paths(path):
        p.unlink()
    if path.stat().st_size <= SPLIT_THRESHOLD:
        return False
    with open(path, "rb") as f:
        i = 0
        while True:
            chunk = f.read(PART_BYTES)
            if not chunk:
                break
            (path.parent / f"{path.name}.part{i:03d}").write_bytes(chunk)
            i += 1
    path.unlink()  # remove the oversized original; parts are the canonical form
    logger.info(f"  split oversized cache {path.name} into {i} parts (<100MB each)")
    return True


def _cache_present(path: Path) -> bool:
    return path.exists() or bool(_part_paths(path))


def _load_blob(path: Path):
    """Return a file-like for `path`: the file itself, or a BytesIO reassembled from parts."""
    if path.exists():
        return path
    parts = _part_paths(path)
    if not parts:
        return None
    buf = bytearray()
    for p in parts:
        buf += p.read_bytes()
    return io.BytesIO(bytes(buf))


def encode_or_cache_wholetext(get_enc, tag: str, rows: list[dict], width: int, use_cache: bool):
    """Reuse cached whole-text encodings (GPU-free re-run) else encode via get_enc().
    Cache files >100MB are transparently byte-split into `<name>.partNNN` (GitHub deploy limit)."""
    cf_lat = CACHE_DIR / f"lat_{tag}_w{width}_n{len(rows)}.npz"
    cf_res = CACHE_DIR / f"resid_{tag}_w{width}_n{len(rows)}.npy"
    if use_cache and _cache_present(cf_lat) and _cache_present(cf_res):
        logger.info(f"  loading cached whole-text encodings {tag} (n={len(rows)})")
        lat = sp.load_npz(_load_blob(cf_lat))
        resid = np.load(_load_blob(cf_res))
        assert lat.shape == (len(rows), width), f"cache lat shape {lat.shape} != {(len(rows), width)}"
        assert resid.shape[0] == len(rows), f"cache resid rows {resid.shape[0]} != {len(rows)}"
        return lat, resid, {"cached": True, "n": len(rows)}
    lat, resid, fvu, l0, dropped = get_enc().encode_rows(rows)
    sp.save_npz(cf_lat, lat)
    _save_blob_split(cf_lat)
    np.save(cf_res, resid)
    _save_blob_split(cf_res)
    return lat, resid, {"cached": False, "fvu": fvu, "mean_l0": l0, "dropped": dropped, "n": len(rows)}


# ============================================================================= analysis
def _col_fire_rate(lat: sp.csr_matrix, rows: np.ndarray) -> np.ndarray:
    """Per-latent firing rate over the given rows (sparse, no dense width matrix)."""
    if len(rows) == 0:
        return np.zeros(lat.shape[1])
    return np.asarray((lat[rows] > 0).mean(0)).ravel()


def _col_fire_count(lat: sp.csr_matrix, rows: np.ndarray) -> np.ndarray:
    if len(rows) == 0:
        return np.zeros(lat.shape[1])
    return np.asarray((lat[rows] > 0).sum(0)).ravel().astype(np.float64)


def identify_parent(lat_bios_sel: sp.csr_matrix, lat_neg: sp.csr_matrix, lat_bios_diag: sp.csr_matrix,
                    width: int, rng: np.random.Generator) -> dict:
    """Corpus-only parent (anchor) identification.

    discriminative := firing_rate(bios_sel) - firing_rate(neg) above a LABEL-SHUFFLE null
                      (B=1000, 95th pct per latent) AND observed diff > 0.
    precision-passing := prec_l = fires_on_bios / (fires_on_bios + fires_on_neg) >= 0.70.
    anchor := among precision-passing discriminative latents, MAX overall bio-recall (selection),
              validated to fire on > FIRING_FLOOR of HELD-OUT bios.
    """
    n_bios = lat_bios_sel.shape[0]
    n_neg = lat_neg.shape[0]
    c_bios = _col_fire_count(lat_bios_sel, np.arange(n_bios))   # [width]
    c_neg = _col_fire_count(lat_neg, np.arange(n_neg))          # [width]
    rate_bios = c_bios / max(n_bios, 1)
    rate_neg = c_neg / max(n_neg, 1)
    obs_diff = rate_bios - rate_neg

    # label-shuffle null on the COMBINED firing matrix (sparse @ dense)
    fire_comb = sp.vstack([(lat_bios_sel > 0), (lat_neg > 0)]).astype(np.float32).tocsc()  # [N,width]
    Ntot = n_bios + n_neg
    tot = c_bios + c_neg
    B_null = 1000
    V = np.zeros((Ntot, B_null), dtype=np.float32)
    for b in range(B_null):
        perm = rng.permutation(Ntot)[:n_bios]
        V[perm, b] = 1.0
    counts = np.asarray(fire_comb.T @ V)  # [width, B] number of bios-labelled firing per shuffle
    null_diff = counts / max(n_bios, 1) - (tot[:, None] - counts) / max(n_neg, 1)
    tau95 = np.percentile(null_diff, 95, axis=1)  # [width]
    del fire_comb, V, counts, null_diff
    gc.collect()

    with np.errstate(invalid="ignore", divide="ignore"):
        prec = np.where(tot > 0, c_bios / np.maximum(tot, 1), 0.0)
    discriminative = (obs_diff > tau95) & (obs_diff > 0)
    disc_idx = np.where(discriminative)[0]
    prec_pass = disc_idx[prec[disc_idx] >= PRECISION_FLOOR]
    pool = prec_pass if len(prec_pass) else disc_idx
    if len(pool) == 0:
        return {"anchor": None, "reason": "no_discriminative_latent",
                "n_discriminative": 0, "n_precision_passing": 0}
    # rank by overall bio-recall (selection); apply held-out firing-floor
    diag_rate = _col_fire_rate(lat_bios_diag, np.arange(lat_bios_diag.shape[0]))
    order = pool[np.argsort(-rate_bios[pool])]
    anchor = None
    for cand in order:
        if diag_rate[cand] > FIRING_FLOOR:
            anchor = int(cand)
            break
    if anchor is None:
        anchor = int(order[0])  # fall back to top recall (flag below)
    return {
        "anchor": anchor,
        "anchor_recall_selection": float(rate_bios[anchor]),
        "anchor_recall_heldout": float(diag_rate[anchor]),
        "anchor_precision_bios_vs_neg": float(prec[anchor]),
        "anchor_neg_fire_rate": float(rate_neg[anchor]),
        "anchor_firing_floor_ok": bool(diag_rate[anchor] > FIRING_FLOOR),
        "n_discriminative": int(len(disc_idx)),
        "n_precision_passing": int(len(prec_pass)),
        "discriminative_precision_passing_pool": [int(x) for x in prec_pass],
        "top10_by_recall": [{"latent": int(l), "recall_sel": float(rate_bios[l]),
                             "precision": float(prec[l]), "neg_rate": float(rate_neg[l])}
                            for l in order[:10]],
        # arrays needed downstream
        "_prec": prec, "_rate_bios": rate_bios, "_rate_neg": rate_neg, "_disc_idx": disc_idx,
        "_prec_pass": prec_pass,
    }


def _within_bios_specialists(counts_pl: np.ndarray, n_prof: np.ndarray, tot_fire: np.ndarray,
                             pidx: int, cand_pool: np.ndarray) -> tuple:
    """For profession pidx: latents in cand_pool with within-bios precision >=0.70 (prof vs
    other-prof) AND coverage (fires on >= GAIN_MIN of prof bios). Returns (specialist latent ids,
    their precision, their coverage)."""
    cov = counts_pl[pidx, cand_pool] / max(n_prof[pidx], 1)        # fires-on-prof / n_prof
    with np.errstate(invalid="ignore", divide="ignore"):
        prec = np.where(tot_fire[cand_pool] > 0,
                        counts_pl[pidx, cand_pool] / np.maximum(tot_fire[cand_pool], 1), 0.0)
    sel = (prec >= SUBCTX_PREC) & (cov >= GAIN_MIN)
    return cand_pool[sel], prec[sel], cov[sel]


def per_profession_hole_table(lat_bios_diag: sp.csr_matrix, prof_diag: np.ndarray,
                              gender_diag: np.ndarray, professions: list[str], anchor: int,
                              cand_pool: np.ndarray) -> dict:
    """The headline deliverable: for ALL professions (held-out fold), the parent recall hole and
    whether a mutually-exclusive within-bios specialist fills it (absorption signature)."""
    n_diag = lat_bios_diag.shape[0]
    prof_to_idx = {p: i for i, p in enumerate(professions)}
    # profession indicator matrix P [n_prof, n_diag]
    rows = np.array([prof_to_idx[p] for p in prof_diag])
    P = sp.csr_matrix((np.ones(n_diag), (rows, np.arange(n_diag))),
                      shape=(len(professions), n_diag))
    fire_diag = (lat_bios_diag > 0).astype(np.float32)            # [n_diag, width]
    counts_pl = np.asarray((P @ fire_diag).todense())             # [n_prof, width] prof x latent fire-count
    n_prof = np.asarray(P.sum(1)).ravel()                         # [n_prof]
    tot_fire = np.asarray(fire_diag.sum(0)).ravel()               # [width]
    anchor_fire = np.asarray((lat_bios_diag[:, anchor] > 0).todense()).ravel()  # [n_diag]

    hole_table = {}
    for pi, p in enumerate(professions):
        msk = prof_diag == p
        n_p = int(msk.sum())
        recall_p = float(counts_pl[pi, anchor] / max(n_prof[pi], 1))
        hole_p = 1.0 - recall_p
        spec_ids, spec_prec, spec_cov = _within_bios_specialists(
            counts_pl, n_prof, tot_fire, pi, cand_pool)
        best_jac, best_spec, best_spec_prec = 1.0, None, None
        n_specialists = int(len(spec_ids))
        if n_specialists > 0:
            # positive-only firing-Jaccard(specialist, anchor) over held-out bios
            sub = np.asarray((lat_bios_diag[:, spec_ids.tolist()] > 0).todense())  # [n_diag, n_spec]
            inter = (sub & anchor_fire[:, None]).sum(0).astype(np.float64)
            union = sub.sum(0) + anchor_fire.sum() - inter
            jac = np.divide(inter, np.maximum(union, 1))
            bi = int(np.argmin(jac))
            best_jac = float(jac[bi]); best_spec = int(spec_ids[bi])
            best_spec_prec = float(spec_prec[bi])
        absorption_type = bool(hole_p > 0.5 and best_jac < JACCARD_MAX)
        # gender split
        gh = {}
        for g in ("male", "female"):
            gm = msk & (gender_diag == g)
            if gm.sum() > 0:
                gh[f"{g}_hole"] = float(1.0 - anchor_fire[gm].mean())
                gh[f"{g}_n"] = int(gm.sum())
        hole_table[p] = {
            "n": n_p, "eligible": bool(n_p >= N_MIN_ELIGIBLE),
            "parent_recall": recall_p, "parent_hole": hole_p,
            "best_specialist": best_spec, "best_specialist_precision": best_spec_prec,
            "best_jaccard": best_jac, "n_specialists": n_specialists,
            "absorption_type": absorption_type, "gender_split": gh,
        }
    return hole_table, {"counts_pl": counts_pl, "n_prof": n_prof, "tot_fire": tot_fire,
                        "anchor_fire_diag": anchor_fire, "prof_to_idx": prof_to_idx}


def setcover_for_profession(p: str, lat_bios_sel: sp.csr_matrix, lat_bios_diag: sp.csr_matrix,
                            resid_sel: np.ndarray, resid_diag: np.ndarray,
                            prof_sel: np.ndarray, prof_diag: np.ndarray, anchor: int,
                            elig_pool: np.ndarray, prec_bios_vs_neg: np.ndarray, width: int,
                            d_p_unit: np.ndarray, rng: np.random.Generator,
                            b_auc: int = 10000, b_draws: int = 1000) -> dict:
    """One-vs-rest set-cover + selection-isolation for a single profession (positives = prof-p,
    negatives = other-profession bios). Mirrors the iter-4 K-track / selector / AUC-diff machinery.
    Selection (greedy + gates) fit on the SELECTION fold; AUC/CIs REPORTED on the HELD-OUT fold."""
    # selection-fold positives = prof-p bios; holes = those the anchor misses
    sel_pos = np.where(prof_sel == p)[0]
    diag_pos = np.where(prof_diag == p)[0]
    diag_neg = np.where(prof_diag != p)[0]
    sel_neg = np.where(prof_sel != p)[0]
    if len(diag_neg) > NEG_CAP_SETCOVER:   # bound the B=10k AUC bootstrap cost (one-vs-rest)
        diag_neg = np.sort(rng.choice(diag_neg, size=NEG_CAP_SETCOVER, replace=False))
    CR = np.asarray(elig_pool)
    if anchor not in CR.tolist():
        CR = np.concatenate([[anchor], CR])
    anchor_fire_sel = np.asarray((lat_bios_sel[sel_pos][:, anchor] > 0).todense()).ravel()
    fire_sel_d = np.asarray((lat_bios_sel[sel_pos][:, CR.tolist()] > 0).todense())  # [n_sel_pos,|CR|]

    # per-CR within-bios precision for prof p (selection fold) + firing-Jaccard vs anchor
    fire_sel_all = (lat_bios_sel > 0).astype(np.float32)
    tot_fire_sel = np.asarray(fire_sel_all[:, CR.tolist()].sum(0)).ravel()
    pos_fire_sel = np.asarray(fire_sel_all[sel_pos][:, CR.tolist()].sum(0)).ravel()
    with np.errstate(invalid="ignore", divide="ignore"):
        subctx_prec_sel = np.where(tot_fire_sel > 0, pos_fire_sel / np.maximum(tot_fire_sel, 1), 0.0)
    subctx_arg_sel = np.zeros(len(CR), dtype=int)   # single sub-context (prof p)
    inter_s = (fire_sel_d & anchor_fire_sel[:, None]).sum(0).astype(np.float64)
    union_s = fire_sel_d.sum(0) + anchor_fire_sel.sum() - inter_s
    jaccard_sel = np.divide(inter_s, np.maximum(union_s, 1))

    # K-track greedy (gated + weighted) — reuse engine.run_greedy verbatim
    eng.rng = rng
    units, edges = {}, {}
    for variant in ("gated", "weighted"):
        u, e = eng.run_greedy(variant, anchor, CR, fire_sel_d, anchor_fire_sel, subctx_prec_sel,
                              subctx_arg_sel, jaccard_sel, prec_bios_vs_neg, [p], GREEDY_MAX_MEMBERS)
        units[variant] = [int(x) for x in u]
        edges[variant] = e
    unit = units["gated"]

    # ---- detector scores on HELD-OUT rows (positives=prof-p, negatives=other-prof) ----
    def pool_score(pool, lat_block):
        if not pool:
            return np.zeros(lat_block.shape[0])
        return np.asarray(lat_block[:, list(pool)].todense()).max(1)

    diag_all = np.concatenate([diag_pos, diag_neg])
    y = np.r_[np.ones(len(diag_pos)), np.zeros(len(diag_neg))]
    lat_eval = lat_bios_diag[diag_all]

    # marginal-attribution (g)/(h) pools from SELECTION fold (prof-p vs other-prof)
    mean_pos = np.asarray(lat_bios_sel[sel_pos].mean(0)).ravel()
    mean_neg = np.asarray(lat_bios_sel[sel_neg].mean(0)).ravel()
    attr_rank = np.argsort(-np.abs(mean_pos - mean_neg))
    g_pool = attr_rank[:20].tolist()
    h_pool = attr_rank[:max(len(unit), 1)].tolist()

    # dense one-vs-rest probe on residuals (selection fit, held-out score)
    from sklearn.linear_model import LogisticRegression
    probe = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced")
    Xtr = np.r_[resid_sel[sel_pos], resid_sel[sel_neg]].astype(np.float32)
    ytr = np.r_[np.ones(len(sel_pos)), np.zeros(len(sel_neg))]
    probe.fit(Xtr, ytr)
    dense_eval = probe.decision_function(resid_diag[diag_all].astype(np.float32))

    # label-free count-matched selectors (S-rec / S-prec / S-mag), anchored (primary)
    cover_count = pos_fire_sel.copy()                 # content (prof-p) recall proxy on CR
    crpos = {int(l): i for i, l in enumerate(CR)}

    def _prec_of(l):
        i = crpos.get(int(l)); return float(subctx_prec_sel[i]) if i is not None else 0.0

    def _cov_of(l):
        i = crpos.get(int(l)); return float(cover_count[i]) if i is not None else 0.0

    def _mag_of(l):
        return float(mean_pos[l] - mean_neg[l])

    ELIG = [int(l) for l in CR]
    k = len(unit)
    sel_members = {}
    for nm, keyf in (("S_rec", lambda l: (_cov_of(l),)),
                     ("S_prec", lambda l: (_prec_of(l), _cov_of(l))),
                     ("S_mag", lambda l: (_mag_of(l),))):
        ranked = sorted(ELIG, key=keyf, reverse=True)
        anch = [int(anchor)] + [int(x) for x in ranked if x != anchor][:k - 1]
        sel_members[nm] = anch

    # RE-k-anchored draws (held-out scored)
    elig_no_anchor = np.array([e for e in ELIG if e != anchor])
    n_eval = len(diag_all)
    rek_anch = np.zeros((b_draws, n_eval), dtype=np.float32)
    for d in range(b_draws):
        if len(elig_no_anchor) >= k - 1:
            pa = [anchor] + rng.choice(elig_no_anchor, size=k - 1, replace=False).tolist()
        else:
            pa = [anchor]
        rek_anch[d] = pool_score(pa, lat_eval)
    rek_anch_mean = rek_anch.mean(0)

    det = {
        "unit": pool_score(unit, lat_eval), "anchor": pool_score([anchor], lat_eval),
        "g": pool_score(g_pool, lat_eval), "h": pool_score(h_pool, lat_eval),
        "dense_probe": dense_eval, "rek_anch_mean": rek_anch_mean,
        "S_rec_anch": pool_score(sel_members["S_rec"], lat_eval),
        "S_prec_anch": pool_score(sel_members["S_prec"], lat_eval),
        "S_mag_anch": pool_score(sel_members["S_mag"], lat_eval),
    }
    pos_m = y == 1
    neg_m = y == 0
    auc_point = {dk: float(eng.fast_auc(det[dk][pos_m], det[dk][neg_m])) for dk in det}
    # AUC-difference CIs (stratified paired bootstrap)
    npos, nneg = int(pos_m.sum()), int(neg_m.sum())
    ip = rng.integers(0, npos, size=(b_auc, npos))
    ineg = rng.integers(0, nneg, size=(b_auc, nneg))
    da = eng._auc_rows(det["unit"][pos_m][ip], det["unit"][neg_m][ineg])
    comps = ["g", "h", "dense_probe", "rek_anch_mean", "S_rec_anch", "S_prec_anch", "S_mag_anch"]
    auc_diff = {}
    for c in comps:
        db = eng._auc_rows(det[c][pos_m][ip], det[c][neg_m][ineg])
        d = da - db
        lo, hi = np.percentile(d, [2.5, 97.5])
        auc_diff[c] = {"diff": float(auc_point["unit"] - auc_point[c]),
                       "ci_lo": float(lo), "ci_hi": float(hi)}
    del ip, ineg, da
    # set_cover_established := unit beats ALL of g,h,S-*-anch,RE-k-anch with CI>0 (dense is non-SAE ref)
    established_comps = ["g", "h", "rek_anch_mean", "S_rec_anch", "S_prec_anch", "S_mag_anch"]
    set_cover_established = all(auc_diff[c]["ci_lo"] > 0 for c in established_comps)

    # ---- form-free KG corroboration (magnitude oracle vs greedy member) ----
    W_dec = eng._GLOBAL["W_dec"]
    wdec_dp = W_dec @ d_p_unit
    anchor_fire_diag_pos = np.asarray((lat_bios_diag[diag_pos][:, anchor] > 0).todense()).ravel()
    hole_rows = diag_pos[~anchor_fire_diag_pos]
    kg = {"n_hole_tokens": int(len(hole_rows))}
    if len(hole_rows) > 0 and len(unit) > 1:
        sub_lat = np.asarray(lat_bios_diag[hole_rows][:, CR.tolist()].todense())
        weighted = sub_lat * wdec_dp[CR][None, :]
        weighted[sub_lat <= 0] = -np.inf
        has_fire = np.isfinite(weighted.max(1))
        arg = weighted.argmax(1)
        ff_top = int(CR[arg[has_fire]][0]) if has_fire.any() else None
        greedy_member = unit[1]
        kg.update({"formfree_magnitude_top_latent": ff_top, "greedy_first_absorber": greedy_member,
                   "member_is_formfree_top": bool(ff_top == greedy_member)})

    # per-row predictions (held-out, Youden operating point) for the prediction record
    from sklearn.metrics import roc_curve
    yall = y
    preds = {}
    for dk in ("unit", "anchor", "g", "h", "dense_probe", "S_rec_anch", "S_prec_anch", "S_mag_anch"):
        sc = det[dk]
        fpr, tpr, thr = roc_curve(yall, sc)
        tau = float(thr[int(np.argmax(tpr - fpr))])
        preds[dk] = (sc >= tau)
    # representative RE-k draw (median AUC)
    draw_aucs = eng._auc_rows(rek_anch[:, pos_m], rek_anch[:, neg_m])
    med = int(np.argsort(draw_aucs)[len(draw_aucs) // 2])
    sc = rek_anch[med]
    fpr, tpr, thr = roc_curve(yall, sc)
    tau = float(thr[int(np.argmax(tpr - fpr))])
    preds["rek"] = (sc >= tau)

    return {
        "profession": p, "n_sel_pos": int(len(sel_pos)), "n_diag_pos": int(len(diag_pos)),
        "n_diag_neg": int(len(diag_neg)),
        "unit": unit, "unit_by_variant": units, "edges": edges["gated"],
        "n_absorbers": len(unit) - 1, "g_pool": g_pool, "h_pool": h_pool,
        "selector_members": sel_members,
        "auc_point": auc_point, "auc_diff_ci": auc_diff,
        "set_cover_established": bool(set_cover_established),
        "kg": kg,
        "_eval_rows": diag_all, "_preds": preds, "_y": y,
    }
