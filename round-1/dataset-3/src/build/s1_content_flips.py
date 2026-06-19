"""STEP 1 — Content-flip pairs from ParaDetox (human toxic<->neutral parallel).

Each pair is the non-circular content perturbation P used downstream to compute
per-latent content-response r_l = a_l(x_on) - a_l(x_off):
    x_on  = en_toxic_comment   (toxicity content PRESENT, label toxic=1)
    x_off = en_neutral_comment (toxicity content ABSENT,  label neutral=0)

Output: temp/intermediate/content_pairs.json  (list of intermediate dicts)
"""
from __future__ import annotations

import json
import os

from common import (clean_text, get_logger, norm_key, sha16,
                    source_sentence_id)

LOG = get_logger("s1_content")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PARADETOX_JSON = os.path.join(ROOT, "temp", "datasets",
                              "full_s-nlp_paradetox_default_train.json")
OUT = os.path.join(ROOT, "temp", "intermediate", "content_pairs.json")


def load_paradetox():
    """Load ParaDetox train rows. Prefer the already-downloaded JSON; fall
    back to the HuggingFace `datasets` library if the file is missing."""
    if os.path.exists(PARADETOX_JSON):
        try:
            with open(PARADETOX_JSON) as f:
                data = json.load(f)
            rows = data["rows"] if isinstance(data, dict) and "rows" in data else data
            if rows and "en_toxic_comment" in rows[0]:
                LOG.info("Loaded %d ParaDetox rows from disk", len(rows))
                return rows
            LOG.warning("Disk JSON missing expected columns; falling back to datasets lib")
        except Exception as e:  # corrupt / truncated snapshot
            LOG.warning("Disk JSON unreadable (%s); falling back to datasets lib", repr(e)[:120])
    from datasets import load_dataset
    ds = load_dataset("s-nlp/paradetox", split="train")
    rows = [dict(r) for r in ds]
    LOG.info("Loaded %d ParaDetox rows via datasets lib", len(rows))
    return rows


def build():
    rows = load_paradetox()
    seen_pairs = set()
    out = []
    n_empty = n_same = n_dup = 0
    for r in rows:
        toxic = clean_text(r.get("en_toxic_comment", ""))
        neutral = clean_text(r.get("en_neutral_comment", ""))
        if not toxic or not neutral:
            n_empty += 1
            continue
        if norm_key(toxic) == norm_key(neutral):
            n_same += 1  # degenerate: nothing flips
            continue
        dkey = (toxic.lower(), neutral.lower())
        if dkey in seen_pairs:
            n_dup += 1
            continue
        seen_pairs.add(dkey)
        ssid = source_sentence_id(toxic)
        pair_id = "cp_" + sha16(toxic.lower() + "||" + neutral.lower())
        out.append({
            "record_type": "content_pair",
            "source": "paradetox",
            "text_on": toxic,       # toxic member (== canonical input)
            "text_off": neutral,    # neutral member
            "pair_id": pair_id,
            "source_sentence_id": ssid,
        })

    n_unique_src = len({o["source_sentence_id"] for o in out})
    LOG.info("Content pairs kept=%d | dropped empty=%d same=%d dup=%d | unique toxic sources=%d",
             len(out), n_empty, n_same, n_dup, n_unique_src)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f)
    LOG.info("Wrote %s", OUT)
    return out


if __name__ == "__main__":
    build()
