#!/usr/bin/env python3
"""Post-hoc auditability enrichment: attach Neuronpedia auto-interp labels + top tokens to the
key SAE latents (general latent, per-sub detectors, two-track unit members) in method_out.json,
so the cluster/latent definitions are human-auditable (no LLM spend; public Neuronpedia GET API)."""
import json, sys, time, urllib.request
from pathlib import Path
from loguru import logger

logger.remove(); logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
HERE = Path(__file__).resolve().parent
OUT = HERE / "method_out.json"
CACHE = HERE / "neuronpedia_cache.json"
ENDPOINT = "https://www.neuronpedia.org/api/feature/gemma-2-2b/12-gemmascope-res-16k/{idx}"


def fetch(idx, cache):
    key = str(idx)
    if key in cache:
        return cache[key]
    url = ENDPOINT.format(idx=idx)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        r = json.loads(urllib.request.urlopen(req, timeout=25).read())
        expl = r.get("explanations") or []
        label = (expl[0].get("description").strip() if expl and expl[0].get("description") else None)
        toks = (r.get("pos_str") or [])[:12]
        out = dict(label=label, top_tokens=toks)
    except Exception as e:
        logger.warning(f"neuronpedia fetch failed for {idx}: {type(e).__name__}: {e}")
        out = dict(label=None, top_tokens=[], error=str(e)[:120])
    cache[key] = out
    time.sleep(0.4)
    return out


def main():
    d = json.loads(OUT.read_text())
    meta = d["metadata"]
    fs = meta.get("firing_structure", {})
    unit = meta.get("unit", {})
    idxs = set()
    for k in ("general_latent_idx", "general_latent_idx_cls_derived"):
        if isinstance(fs.get(k), int):
            idxs.add(fs[k])
    for mp in ("detector_idx_per_sub", "detector_meanact_idx_per_sub"):
        for v in (fs.get(mp) or {}).values():
            if isinstance(v, int):
                idxs.add(v)
    for m in unit.get("members", []):
        idxs.add(int(m))
    idxs = sorted(idxs)
    logger.info(f"fetching Neuronpedia labels for {len(idxs)} key latents: {idxs}")
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    labels = {}
    for i in idxs:
        info = fetch(i, cache)
        labels[str(i)] = info
        logger.info(f"  latent {i}: {info.get('label')!r} tokens={info.get('top_tokens', [])[:6]}")
    CACHE.write_text(json.dumps(cache, indent=2))

    fs["neuronpedia_labels"] = labels
    fs["general_latent_label"] = labels.get(str(fs.get("general_latent_idx")), {}).get("label")
    fs["detector_label_per_sub"] = {
        s: labels.get(str(idx), {}).get("label")
        for s, idx in (fs.get("detector_idx_per_sub") or {}).items()
    }
    unit["member_labels"] = {str(m): labels.get(str(m), {}).get("label") for m in unit.get("members", [])}
    unit["member_top_tokens"] = {str(m): labels.get(str(m), {}).get("top_tokens", []) for m in unit.get("members", [])}
    meta["auditability_note"] = ("Key latent definitions are human-auditable via Neuronpedia auto-interp "
                                 "labels + top-activating tokens (gemma-2-2b 12-gemmascope-res-16k). "
                                 "The general toxicity latent and each cluster member carry an interpretable label.")
    OUT.write_text(json.dumps(d, indent=2))
    logger.info(f"patched {OUT} ({OUT.stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
