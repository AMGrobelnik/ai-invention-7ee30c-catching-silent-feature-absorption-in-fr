#!/usr/bin/env python
"""Quick diagnostic: Georgia absorber 16009 vs 4697 — cr membership, SCR/TPP attribution rank,
per-N recall curve, oracle decoder-cos. Decides the absorber + N-grid design."""
import os, json
os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np
import core, screen as SCR, m9 as M9
import method as MT
from pathlib import Path

torch = __import__("torch")
sae = core.load_sae(torch)
mb = core.ModelBundle(torch)
M9.gating_check(mb, sae)
W_dec_np = sae.W_dec.detach().cpu().numpy().astype(np.float32)
kg = json.loads(MT.KG4.read_text())["metadata"]["canonical_units"]
fam = M9.build_taxonomic(mb, sae, int(kg["taxonomic"]["anchor"]))
fam._sae = sae; fam.torch = torch

cr = np.asarray(M9.family_cr(fam), int)
sel_rows, X_sel, y_sel = MT.selection_xy(fam, "country", cr)
abs_rows, sib_rows = MT.eval_slices(fam, "Georgia", [c for c in fam.eligible if c != "Georgia"])
print(f"cr={len(cr)} sel_rows={len(sel_rows)}(pos={int(y_sel.sum())}) abs={len(abs_rows)} sib={len(sib_rows)}")

# full ranking
selected_all, ranks = MT.scr_tpp_select(cr, X_sel, y_sel, N=len(cr))
for ab in (16009, 4697):
    print(f"absorber {ab}: in_cr={ab in set(cr.tolist())} attr_rank={ranks.get(ab)}")

# screen rows
for ab in (16009, 4697, None):
    info = {"parent": "country", "letter": None}
    r = M9.screen_candidate(fam, "Georgia", info, W_dec_np, compute_oracle=True, known_absorber=ab)
    print(f"  known={ab}: absorber={r['absorber_latent']} predict={r['predict_absorption']} "
          f"rh={r['recall_hole']} jac={r['firing_jaccard']} prec={r['precision']} "
          f"gain={r['hole_coverage_gain']} oracle_cos={r['oracle_decoder_cos']} "
          f"strict={r['absorption_structured_strict']}")

# per-N recall curve for both absorbers
for ab in (16009, 4697):
    print(f"=== absorber {ab} ===")
    for N in (1, 2, 5, 10, 20, 50):
        raw, _ = MT.scr_tpp_select(cr, X_sel, y_sel, N=N)
        in_top = ab in set(int(x) for x in raw)
        selN = np.array([l for l in raw if int(l) != ab], int)
        repN = np.append(selN, ab)
        hb = MT.fit_head(fam, selN, sel_rows, y_sel)
        hr = MT.fit_head(fam, repN, sel_rows, y_sel)
        ra = MT.slice_predict(fam, hb, selN, abs_rows).mean()
        rs = MT.slice_predict(fam, hb, selN, sib_rows).mean()
        rr = MT.slice_predict(fam, hr, repN, abs_rows).mean()
        print(f"  N={N:3d} in_top={in_top} base_abs={ra:.3f} base_sib={rs:.3f} repaired_abs={rr:.3f} delta={rr-ra:+.3f}")
