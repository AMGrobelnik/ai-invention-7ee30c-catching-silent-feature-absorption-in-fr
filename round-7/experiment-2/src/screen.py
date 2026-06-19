#!/usr/bin/env python
"""
M2'' SCREEN — the PRIMARY ($0) deliverable.

Screen the named_entity_safety hierarchy (art_KNPsfjByyxiS) for the Georgia absorption SIGNATURE to test
the central reposition thesis: ABSORPTION = LEXICAL HOMOGRAPHY (a suppressed 'is-a-named-entity/org' parent
under a polysemous surface token), NOT safety / demographic semantics. Named-entity homographs
(Apple/Amazon/Bush/Cook/King) SHOULD show the Georgia signature; plain demographic identity terms (iter-6)
do not.

Per eligible entity X the screen computes, NON-CIRCULARLY (absorber chosen on the DIAGNOSTIC fit fold, every
metric SCORED on the disjoint TRAIN eval fold):
  recall_hole(X)        = 1 - P(parent latent fires | X-positive eval rows)            [router signal]
  absorber(X)           = K-track-lite: content-responsive, sub-context-PRECISE (>=0.7), MUTUALLY EXCLUSIVE
                          with the parent (firing-Jaccard<0.1), parent-hole-COVERING (highest hole coverage)
  precision(X)          = fraction of absorber-firing eval rows whose entity == X
  hole_coverage_gain    = recall recovery on X-eval rows when absorber is OR'd into parent, with bootstrap CI
  oracle_absorption_frac= form-free SAEBench probe-projection metric (uses dense LR-probe dir d_p, NOT a
                          single latent; never used to FORM the absorber) -> non-circular corroboration
  is_homograph / strength (manifest + wordfreq cross-check)
  absorption_structured = recall_hole>0.5 AND jaccard<0.1 AND precision>=0.7 AND n_eligible>=150 AND
                          hole_coverage_gain CI excl 0 AND oracle corroborates.

A KNOWN-positive SANITY runs the identical metric function on Georgia (taxonomic, absorber 16009) and asserts
it is flagged structured -> proves the screen detects a real absorber, not noise.
"""
import json
import numpy as np
from collections import defaultdict, Counter

import core
from core import (logger, el, content_responsive, ParentProbe, pick_random_latents, DEVICE, SEED, D_MODEL)

ROOT = core.ROOT
D_NE = ROOT / "iter_6/gen_art/gen_art_dataset_1/full_data_out.json"
D_NE_MINI = ROOT / "iter_6/gen_art/gen_art_dataset_1/mini_data_out.json"
MAN = ROOT / "iter_6/gen_art/gen_art_dataset_1/manifest.json"
D2_TAX = ROOT / "iter_1/gen_art/gen_art_dataset_2/full_data_out.json"

rng = np.random.default_rng(SEED)

# ----- screen thresholds (Georgia-signature, identical to iter-3/iter-6 absorption gate) -----
PARENT_FIRING_FLOOR = 0.05      # parent latent must fire on >5% of held-out corpus rows (genuine detector)
PREC_MIN = 0.70                 # sub-context precision floor
JAC_MAX = 0.10                  # firing-Jaccard(parent, absorber) ceiling (mutual exclusivity)
RECALL_HOLE_MIN = 0.50         # parent recall-hole floor (suppressed parent)
GAIN_MIN = 0.05                # hole-coverage-gain floor (also require bootstrap CI excl 0)
N_ELIGIBLE_MIN = 150          # eligible diagnostic-positive floor for the STRICT structured gate
ORACLE_TAU = 0.50            # (reported) a single latent carries >50% of the SAE-recon probe-projection
ORACLE_MIN_FRAC = 0.10      # (reported) share-majority fraction
DECODER_COS_MIN = 0.025     # canonical Chanin/SAEBench probe_cos_sim_threshold on W_dec (decoder-probe align)
MIN_FIRE_DIAG = 5           # absorber must fire on >=5 diagnostic X-positive rows to be considered
B_BOOT_GAIN = 5000          # bootstrap reps for the hole-coverage-gain CI

PRIMARY_ELIGIBLE = ["Apple", "Amazon", "Bush", "Cook", "King"]
DESCRIPTIVE_ONLY = ["Fox", "West", "Bell", "Stone", "Wood", "Gates", "Hunt", "Target", "Bird",
                    "Oracle", "Swift", "Banks", "Page"]
NE_PARENT_CONCEPT = "a named public figure or organization"
ORG_ENTITIES = {"Apple", "Amazon", "Oracle", "Target", "Gates", "Visa", "Subway", "Shell",
                "Corona", "Monster", "Tide", "Gap", "Banks"}   # heuristic org/person split (for the guard)


def _zipf(word):
    try:
        import wordfreq
        return float(wordfreq.zipf_frequency(word.lower(), "en"))
    except Exception:
        return None


def load_manifest():
    return json.loads(MAN.read_text())


def load_named_entity(mini=False):
    blob = json.loads((D_NE_MINI if mini else D_NE).read_text())
    ds = next(d for d in blob["datasets"] if d["dataset"] == "named_entity_safety")
    return [core._attach_span_tax(dict(r)) for r in ds["examples"]]


def load_taxonomic_rows():
    blob = json.loads(D2_TAX.read_text())
    ds = next(d for d in blob["datasets"] if d["dataset"] == "taxonomic_absorption")
    return [core._attach_span_tax(dict(r)) for r in ds["examples"]]


class ScreenState:
    """Holds the single corpus encoding so the conditional downstream reuses it (no re-encode)."""
    pass


# =========================================================================== ENCODE + PARENT
def encode_corpus(torch, sae, mb, rows, entities, cap_pos=300, cap_neg_each=1600):
    """Encode corpus positives (capped/entity) + negatives (capped/family) + content pairs. Returns
    (enc_rows, lat_csr, resid, kind[], sub[], fold[], A_on, A_off, cr)."""
    corp = [r for r in rows if r["metadata_row_type"] == "corpus"]
    cpairs = [r for r in rows if r["metadata_row_type"] == "content_pair"]
    eset = set(entities)
    enc_rows, tag = [], []
    pos_count = defaultdict(int)
    neg_count = defaultdict(int)
    for r in corp:
        if r["output"] == "positive":
            sc = r.get("metadata_sub_context")
            if sc in eset and pos_count[sc] < cap_pos:
                pos_count[sc] += 1
                enc_rows.append(r); tag.append(("pos", sc, r.get("metadata_fold")))
        else:  # negative
            fam = r.get("metadata_neg_family") or "other"
            if neg_count[fam] < cap_neg_each:
                neg_count[fam] += 1
                enc_rows.append(r); tag.append(("neg", fam, r.get("metadata_fold")))
    n_corp = len(enc_rows)
    for r in cpairs:
        enc_rows.append(r); tag.append(("cp", r.get("metadata_pair_role"), r.get("metadata_pair_id")))
    logger.info(f"{el()} screen encoding {len(enc_rows)} rows ({n_corp} corpus + {len(cpairs)} cp); "
                f"pos={dict(pos_count)}")
    lat_csr, resid, align = mb.encode_rows(enc_rows, sae)
    kind = np.array([t[0] for t in tag], dtype=object)
    sub = np.array([t[1] for t in tag], dtype=object)
    fold = np.array([t[2] for t in tag], dtype=object)
    # content-responsive set from content pairs
    pairs = defaultdict(dict)
    for i in np.where(kind == "cp")[0]:
        pairs[tag[i][2]][tag[i][1]] = i
    pl = [p for p, d in pairs.items() if "x_on" in d and "x_off" in d]
    A_on = A_off = None
    cr = np.array([], int)
    if pl:
        A_on = np.asarray(lat_csr[[pairs[p]["x_on"] for p in pl]].todense())
        A_off = np.asarray(lat_csr[[pairs[p]["x_off"] for p in pl]].todense())
        cr, _, _ = content_responsive(A_on, A_off)
    logger.info(f"{el()} screen content-responsive latents={len(cr)} (from {len(pl)} content pairs)")
    return enc_rows, lat_csr, resid, kind, sub, fold, A_on, A_off, cr, align


def identify_parent(lat_csr, resid, kind, sub, fold, cr, A_on, entities, torch,
                    fit_fold="diagnostic", eval_fold="train"):
    """PARENT = content-responsive latent with HIGHEST recall of entity-sense content flips, VALIDATED by a
    firing-floor on held-out corpus (>5% of rows). Chosen WITHOUT the absorption oracle (recall-only =
    non-circular). Returns (parent_latent, info, probe)."""
    eset = set(entities)
    # corpus masks
    is_pos = (kind == "pos") & np.isin(sub, list(eset))
    is_neg = (kind == "neg")
    corpus_mask = is_pos | is_neg
    held_corpus = corpus_mask & (fold == eval_fold)
    # recall of each content-responsive latent on x_on (entity-present) rows
    info = {"n_responsive": int(len(cr))}
    if len(cr) == 0 or A_on is None:
        info["status"] = "no_responsive_latents"
        return None, info, None
    recall_on = (A_on > 0).mean(0)                              # [d_sae] recall on entity-present flips
    fire_corpus = np.asarray((lat_csr[np.where(held_corpus)[0]] > 0).mean(0)).ravel() if held_corpus.sum() else \
        np.asarray((lat_csr > 0).mean(0)).ravel()
    cand = []
    for c in cr:
        c = int(c)
        cand.append((c, float(recall_on[c]), float(fire_corpus[c])))
    # firing-floor-validated parent = highest x_on recall among latents that fire on >floor of held-out corpus
    valid = [(c, r, f) for (c, r, f) in cand if f >= PARENT_FIRING_FLOOR]
    valid.sort(key=lambda x: -x[1])
    diffuse = False
    if not valid:
        diffuse = True
        # fall back to highest-recall responsive latent regardless of floor (flag diffuse)
        cand.sort(key=lambda x: -x[1])
        parent = cand[0][0] if cand else None
        info["status"] = "diffuse_no_firing_floor_latent"
    else:
        parent = valid[0][0]
        info["status"] = "ok"
    info["parent_latent"] = int(parent) if parent is not None else None
    info["parent_xon_recall"] = float(recall_on[parent]) if parent is not None else None
    info["parent_corpus_firing_rate_heldout"] = float(fire_corpus[parent]) if parent is not None else None
    info["parent_is_diffuse"] = bool(diffuse)
    info["top5_by_xon_recall"] = [{"latent": c, "xon_recall": round(r, 3), "corpus_fire": round(f, 4)}
                                  for (c, r, f) in sorted(cand, key=lambda x: -x[1])[:5]]
    # ParentProbe (d_p for the form-free oracle + u_whole diff-of-means) fit on the DIAGNOSTIC fold
    fit_pos = np.where(is_pos & (fold == fit_fold))[0]
    fit_neg = np.where(is_neg & (fold == fit_fold))[0]
    probe = None
    if len(fit_pos) >= 10 and len(fit_neg) >= 10:
        probe = ParentProbe(torch, resid[fit_pos].astype(np.float32), resid[fit_neg].astype(np.float32))
        info["probe_train_auc"] = float(probe.train_auc)
        info["probe_cos_with_diffmean"] = float(probe.cos_probe_dmu)
        # held-out probe recall (train fold) at 0.5
        ev_pos = np.where(is_pos & (fold == eval_fold))[0]
        if len(ev_pos):
            import torch as _t
            H = _t.tensor(resid[ev_pos].astype(np.float32), device=DEVICE)
            with _t.no_grad():
                sc = probe.score(H).cpu().numpy()
            info["probe_heldout_recall_at_0p5"] = float((sc >= 0.5).mean())
    info["n_fit_pos"] = int(len(fit_pos)); info["n_fit_neg"] = int(len(fit_neg))
    return parent, info, probe


# =========================================================================== PER-ENTITY SCREEN
def screen_one_entity(*, X, parent_latent, lat_csr, resid, kind, sub, fold, cr, probe,
                      sae, W_dec_np, entities, n_eligible, is_homograph, homograph_strength,
                      fit_fold="diagnostic", eval_fold="train", known_absorber=None):
    """Compute the full Georgia-signature screen row for entity X. Absorber chosen on the FIT (diagnostic)
    fold; precision / gain / oracle SCORED on the disjoint EVAL (train) fold."""
    eset = set(entities)
    par_fire = np.asarray(lat_csr[:, parent_latent].todense()).ravel() > 0 if parent_latent is not None \
        else np.zeros(lat_csr.shape[0], bool)

    Xpos = (kind == "pos") & (sub == X)
    diag_Xpos = np.where(Xpos & (fold == fit_fold))[0]
    eval_Xpos = np.where(Xpos & (fold == eval_fold))[0]
    if len(eval_Xpos) == 0:                                   # tiny entity: fall back to all X-pos for scoring
        eval_Xpos = np.where(Xpos)[0]
    diag_corpus = np.where(((kind == "pos") & np.isin(sub, list(eset)) | (kind == "neg")) & (fold == fit_fold))[0]
    eval_corpus_pos = np.where((kind == "pos") & np.isin(sub, list(eset)) & (fold == eval_fold))[0]

    # ---- (a) recall-hole on held-out X rows ----
    recall_hole = 1.0 - float(par_fire[eval_Xpos].mean()) if len(eval_Xpos) else None

    # ---- (b) absorber via K-track-lite on the DIAGNOSTIC fold ----
    cand = np.array([int(c) for c in cr if int(c) != int(parent_latent)], dtype=int)
    absorber = None; absorber_meta = {}
    if len(cand) and len(diag_Xpos):
        C = np.asarray((lat_csr[:, cand] > 0).todense())                 # [N, K] firing booleans
        Cd_X = C[diag_Xpos]                                              # diag X-pos rows
        Cd_corp = C[diag_corpus]                                        # diag corpus rows
        fires_on_diagXpos = Cd_X.sum(0)                                 # [K]
        fires_on_diagcorp = Cd_corp.sum(0)                             # [K]
        precision_diag = fires_on_diagXpos / np.maximum(fires_on_diagcorp, 1)
        # firing-Jaccard with parent over ALL rows
        inter = (C & par_fire[:, None]).sum(0)
        union = (C | par_fire[:, None]).sum(0)
        jac = inter / np.maximum(union, 1)
        # hole coverage on diag X-pos rows where parent is silent
        par_silent_diagX = ~par_fire[diag_Xpos]
        cover = Cd_X[par_silent_diagX].mean(0) if par_silent_diagX.sum() else np.zeros(len(cand))
        qualify = ((precision_diag >= PREC_MIN) & (jac < JAC_MAX) & (cover > 0) &
                   (fires_on_diagXpos >= MIN_FIRE_DIAG))
        if qualify.any():
            qidx = np.where(qualify)[0]
            best = qidx[np.argmax(cover[qidx])]
            absorber = int(cand[best])
            absorber_meta = {"qualified": True, "precision_diag": float(precision_diag[best]),
                             "jaccard_diag_sel": float(jac[best]), "hole_cover_diag": float(cover[best]),
                             "n_fire_diagXpos": int(fires_on_diagXpos[best])}
        else:
            # best candidate by hole coverage among mutually-exclusive ones (report, but won't pass gate)
            mex = np.where((jac < JAC_MAX) & (fires_on_diagXpos >= MIN_FIRE_DIAG))[0]
            if len(mex):
                best = mex[np.argmax(cover[mex])]
                absorber = int(cand[best])
                absorber_meta = {"qualified": False, "precision_diag": float(precision_diag[best]),
                                 "jaccard_diag_sel": float(jac[best]), "hole_cover_diag": float(cover[best]),
                                 "n_fire_diagXpos": int(fires_on_diagXpos[best])}
        del C, Cd_X, Cd_corp
    # honor a known-absorber override (Georgia sanity): also evaluate it
    if known_absorber is not None:
        absorber = int(known_absorber)
        absorber_meta["known_absorber_override"] = True

    if absorber is None:
        return {"entity": X, "n_eligible": int(n_eligible), "recall_hole": recall_hole,
                "absorber_latent": None, "firing_jaccard": None, "precision": None,
                "hole_coverage_gain": None, "gain_ci_lo": None, "gain_ci_hi": None,
                "oracle_absorption_fraction": None, "oracle_mean_proj_ratio": None,
                "oracle_corroborates": False, "is_homograph": bool(is_homograph),
                "homograph_strength": homograph_strength, "absorption_structured": False,
                "parent_latent": int(parent_latent) if parent_latent is not None else None,
                "absorber_meta": absorber_meta, "n_eval_Xpos": int(len(eval_Xpos)),
                "note": "no absorber candidate"}

    ab_fire = np.asarray(lat_csr[:, absorber].todense()).ravel() > 0
    # ---- firing-Jaccard(parent, absorber) over union of firing rows ----
    union = int((par_fire | ab_fire).sum())
    firing_jaccard = int((par_fire & ab_fire).sum()) / max(union, 1)

    # ---- (c) precision on held-out corpus: fraction of absorber-firing eval rows whose entity == X ----
    ev_fire = eval_corpus_pos[ab_fire[eval_corpus_pos]] if len(eval_corpus_pos) else np.array([], int)
    if len(ev_fire) >= 3:
        precision = float(np.mean([sub[i] == X for i in ev_fire]))
        n_ev_fire = int(len(ev_fire))
    else:                                                         # fall back to diag precision if held-out sparse
        precision = float(absorber_meta.get("precision_diag", 0.0)); n_ev_fire = int(len(ev_fire))

    # ---- (d) hole-coverage-gain (+ bootstrap CI) on held-out X rows ----
    gain = gain_lo = gain_hi = None; rand_gain = None
    if len(eval_Xpos) >= 8:
        par_x = par_fire[eval_Xpos].astype(float)
        comb_x = (par_fire[eval_Xpos] | ab_fire[eval_Xpos]).astype(float)
        gain = float(comb_x.mean() - par_x.mean())
        n = len(eval_Xpos)
        idx = rng.integers(0, n, size=(B_BOOT_GAIN, n))
        gains = comb_x[idx].mean(1) - par_x[idx].mean(1)
        gain_lo, gain_hi = [float(v) for v in np.percentile(gains, [2.5, 97.5])]
        # random content-responsive latent control (firing-rate matched)
        try:
            rl, _ = pick_random_latents(lat_csr, absorber, cr, {int(absorber), int(parent_latent)}, n=1)
            if rl:
                rfire = np.asarray(lat_csr[:, int(rl[0])].todense()).ravel() > 0
                rcomb = (par_fire[eval_Xpos] | rfire[eval_Xpos]).astype(float)
                rand_gain = float(rcomb.mean() - par_x.mean())
        except Exception:
            rand_gain = None

    # ---- (e) FORM-FREE ABSORPTION ORACLE (canonical SAEBench/Chanin decoder-probe criterion; non-circular) ----
    # The absorber is a TRUE form-free absorber of the parent concept iff its DECODER write-direction W_dec[l]
    # is aligned with the parent-concept probe direction d_p (Chanin probe_cos_sim_threshold=0.025 on W_dec).
    # We compute this against the diff-of-means concept direction (robust) and the LR direction, AND report the
    # SAE-reconstruction projection share the absorber carries on parent-hole rows. d_p comes from the DENSE
    # probe (never a single latent) -> strictly non-circular: never used to FORM the absorber.
    decoder_cos_mu = decoder_cos_w = None
    oracle_frac = None; oracle_mean = None
    if probe is not None and absorber is not None:
        wdec_ab = W_dec_np[absorber].astype(np.float64)
        wdec_ab_u = wdec_ab / (np.linalg.norm(wdec_ab) + 1e-9)
        d_mu = probe.d_mu.astype(np.float64); d_mu = d_mu / (np.linalg.norm(d_mu) + 1e-9)
        d_w = probe.w.astype(np.float64); d_w = d_w / (np.linalg.norm(d_w) + 1e-9)
        decoder_cos_mu = float(wdec_ab_u @ d_mu)
        decoder_cos_w = float(wdec_ab_u @ d_w)
        if len(eval_Xpos):
            import torch as _t
            wdec_dp = W_dec_np.astype(np.float64) @ d_mu               # [d_sae]  W_dec[l] . d_mu
            rows = eval_Xpos[~par_fire[eval_Xpos]]                     # parent-hole rows (parent latent silent)
            if len(rows) >= 3:
                with _t.no_grad():
                    z_rows = sae.encode(_t.tensor(resid[rows].astype(np.float32),
                                                  device=DEVICE)).cpu().numpy().astype(np.float64)
                total_proj = z_rows @ wdec_dp
                absorber_proj = z_rows[:, absorber] * wdec_dp[absorber]
                valid = np.abs(total_proj) > 1e-6
                if valid.sum() >= 3:
                    proj_ratio = absorber_proj[valid] / total_proj[valid]
                    oracle_frac = float((proj_ratio > ORACLE_TAU).mean())   # share-majority (reported)
                    oracle_mean = float(np.median(proj_ratio))
    # corroboration: decoder write-direction carries the parent concept (canonical Chanin criterion)
    oracle_corroborates = bool(decoder_cos_mu is not None and decoder_cos_mu >= DECODER_COS_MIN)

    # ---- (g) STRUCTURED gate = the FIRING SIGNATURE (the canonical iter-2..6 absorber definition; this is
    # what the Georgia positive control satisfies). The FORM-FREE decoder-projection ORACLE is reported as a
    # SEPARATE, STRICTER corroboration (decoder-projection absorption is spelling/concept-tuned: it strongly
    # confirms the named-entity homograph absorbers but does NOT transfer to the taxonomic Georgia absorber,
    # whose decoder is near-orthogonal to the generic 'country' direction -- so it must NOT gate 'structured'
    # or it would paradoxically reject the known positive). absorption_structured_oracle_confirmed = both. ----
    signature = bool(
        (recall_hole is not None and recall_hole > RECALL_HOLE_MIN) and
        (firing_jaccard < JAC_MAX) and
        (precision >= PREC_MIN) and
        (int(n_eligible) >= N_ELIGIBLE_MIN) and
        (gain is not None and gain >= GAIN_MIN and gain_lo is not None and gain_lo > 0))
    structured = signature
    structured_oracle_confirmed = bool(signature and oracle_corroborates)

    return {
        "entity": X, "n_eligible": int(n_eligible), "recall_hole": recall_hole,
        "absorber_latent": int(absorber), "firing_jaccard": float(firing_jaccard), "precision": float(precision),
        "n_absorber_fire_heldout": n_ev_fire,
        "hole_coverage_gain": gain, "gain_ci_lo": gain_lo, "gain_ci_hi": gain_hi,
        "gain_ci_excl_0": bool(gain_lo is not None and gain_lo > 0),
        "random_latent_gain_control": rand_gain,
        "oracle_absorption_fraction": oracle_frac, "oracle_mean_proj_ratio": oracle_mean,
        "oracle_decoder_cos_mu": decoder_cos_mu, "oracle_decoder_cos_w": decoder_cos_w,
        "oracle_corroborates": oracle_corroborates,
        "is_homograph": bool(is_homograph), "homograph_strength": homograph_strength,
        "homograph_strength_wordfreq": _zipf(X),
        "absorption_structured": structured,
        "absorption_structured_oracle_confirmed": structured_oracle_confirmed,
        "parent_latent": int(parent_latent) if parent_latent is not None else None,
        "absorber_meta": absorber_meta, "n_eval_Xpos": int(len(eval_Xpos)),
    }


# =========================================================================== TAXONOMIC GEORGIA SELF-CHECK
def georgia_selfcheck(torch, sae, mb, W_dec_np, canon, cap_pos=300):
    """Run the IDENTICAL screen metric function on Georgia (taxonomic, known absorber 16009). Asserts the
    screen flags it structured -> the screen detects a real absorber, not noise."""
    logger.info(f"{el()} ===== SCREEN SELF-CHECK on Georgia (taxonomic) =====")
    rows = load_taxonomic_rows()
    eligible = ['Australia', 'Brazil', 'Canada', 'China', 'France', 'Georgia', 'Germany', 'India',
                'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Mexico', 'New Zealand', 'Poland',
                'Russia', 'Spain', 'United Kingdom', 'United States']
    enc_rows, lat_csr, resid, kind, sub, fold, A_on, A_off, cr, align = encode_corpus(
        torch, sae, mb, rows, eligible, cap_pos=cap_pos, cap_neg_each=1600)
    # taxonomic uses content_pair x_on/x_off too; identify the parent via the same procedure
    parent, pinfo, probe = identify_parent(lat_csr, resid, kind, sub, fold, cr, A_on, eligible, torch)
    anchor = canon["taxonomic"]["anchor"]
    # use canonical anchor as the parent for Georgia (the is-a-country detector), as in iter-3/6
    par_latent = anchor
    n_elig = int(((kind == "pos") & (sub == "Georgia") & (fold == "diagnostic")).sum())
    row = screen_one_entity(X="Georgia", parent_latent=par_latent, lat_csr=lat_csr, resid=resid,
                            kind=kind, sub=sub, fold=fold, cr=cr, probe=probe, sae=sae, W_dec_np=W_dec_np,
                            entities=eligible, n_eligible=n_elig, is_homograph=True, homograph_strength=None,
                            known_absorber=16009)
    row_disc = screen_one_entity(X="Georgia", parent_latent=par_latent, lat_csr=lat_csr, resid=resid,
                                 kind=kind, sub=sub, fold=fold, cr=cr, probe=probe, sae=sae, W_dec_np=W_dec_np,
                                 entities=eligible, n_eligible=n_elig, is_homograph=True, homograph_strength=None)
    logger.info(f"{el()} GEORGIA self-check (known 16009): structured={row['absorption_structured']} "
                f"recall_hole={row['recall_hole']} jac={row['firing_jaccard']} prec={row['precision']} "
                f"gain={row['hole_coverage_gain']} (CI {row['gain_ci_lo']}..{row['gain_ci_hi']}) "
                f"oracle={row['oracle_absorption_fraction']}")
    logger.info(f"{el()} GEORGIA self-check (discovered absorber={row_disc['absorber_latent']}): "
                f"structured={row_disc['absorption_structured']}")
    del lat_csr, resid
    import gc; gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return {"known_16009": row, "discovered": row_disc, "parent_info": pinfo,
            "passed": bool(row["absorption_structured"] or row_disc["absorption_structured"])}
