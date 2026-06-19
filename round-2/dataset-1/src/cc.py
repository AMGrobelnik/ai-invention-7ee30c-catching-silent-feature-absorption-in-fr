#!/usr/bin/env python3
"""Shared helpers for the iter-2 surface-invariance superset build.

Byte-faithfulness contract:
  * Text normalization / hashing / ssid: imported VERBATIM from the iter-1
    toxicity build (gen_art_dataset_3/build/common.py) so new rows collide
    correctly with the iter-1 originals.
  * fold_from_key: copied verbatim from the iter-1 toxicity data.py
    (union-find component fold for sources with no native classification fold).
  * First-letter carriers() + fold_of(): copied verbatim from the iter-1
    first-letter data.py (gen_art_dataset_1/data.py) so new first-letter rows
    are byte-compatible with the 590 frozen originals.
  * Surface double-gate (token_jaccard / norm_edit_distance / surface_gate):
    copied verbatim from the iter-1 s3_surface_flips.py (JACCARD_MAX=0.6,
    CHAR_CHANGE_MIN=0.25, strict < and >).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

# ---- pinned iter-1 dependency paths (READ-ONLY) ---------------------------------
RUN_ROOT = Path("/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop")
ITER1 = RUN_ROOT / "iter_1" / "gen_art"
FL_DIR = ITER1 / "gen_art_dataset_1"          # first-letter testbed
TOX_DIR = ITER1 / "gen_art_dataset_3"         # toxicity family
TOX_BUILD = TOX_DIR / "build"
RESEARCH_DIR = ITER1 / "gen_art_research_2"

FL_FULL = FL_DIR / "full_data_out.json"
TOX_FULL = TOX_DIR / "full_data_out.json"
PARADETOX_JSON = TOX_DIR / "temp" / "datasets" / "full_s-nlp_paradetox_default_train.json"
CLS_JSON = TOX_DIR / "temp" / "intermediate" / "classification.json"

# Import the iter-1 toxicity common helpers VERBATIM (norm_key / sha16 / ssid / SUB_ATTRS)
sys.path.insert(0, str(TOX_BUILD))
import common as _tox_common  # noqa: E402

clean_text = _tox_common.clean_text
norm_key = _tox_common.norm_key
sha16 = _tox_common.sha16
source_sentence_id = _tox_common.source_sentence_id  # "ssid_" + sha16(norm_key(text))
SUB_ATTRS = list(_tox_common.SUB_ATTRS)
FLOAT_AXES = list(_tox_common.FLOAT_AXES)
PRIMARY_THRESHOLD = 0.5


def ssid_of(toxic_text: str) -> str:
    """Mirror gen_art_dataset_3/data.py ssid_of (== common.source_sentence_id)."""
    return "ssid_" + sha16(norm_key(toxic_text))


def fold_from_key(key: str, ratios=(0.8, 0.1, 0.1)) -> str:
    """VERBATIM from iter-1 toxicity data.py. Deterministic train/val/test."""
    bucket = int(hashlib.sha1(key.encode("utf-8")).hexdigest(), 16) % 1000
    tcut = int(ratios[0] * 1000)
    vcut = tcut + int(ratios[1] * 1000)
    return "train" if bucket < tcut else ("val" if bucket < vcut else "test")


# ============================ FIRST-LETTER helpers ==============================
N_FOLDS = 5


def fold_of(key: str, n: int = N_FOLDS) -> int:
    """VERBATIM from iter-1 first-letter data.py."""
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(h, 16) % n


def carriers():
    """VERBATIM from iter-1 first-letter data.py. (template_id, prefix, suffix)."""
    return [
        ("t_verbose", "", " has the first letter:"),
        ("t_colon", "", ":"),
        ("t_mention_word", "The word ", " appears in the text."),
        ("t_mention_term", "Consider the term ", " for a moment."),
        ("t_mention_example", "Here is an example word: ", "."),
        ("t_mention_spelled", "Let us spell out the word ", "."),
    ]


# build_surface_pairs in iter-1 used carriers()[:5]
SURFACE_CARRIERS = carriers()[:5]


# ============================ SURFACE double-gate ===============================
JACCARD_MAX = 0.6        # token overlap must be strictly below this
CHAR_CHANGE_MIN = 0.25   # normalized edit distance must be strictly above this


def _tok(s: str):
    return [t for t in re.split(r"\W+", s.lower()) if t]


def token_jaccard(a: str, b: str) -> float:
    sa, sb = set(_tok(a)), set(_tok(b))
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / max(1, len(sa | sb))


def norm_edit_distance(a: str, b: str) -> float:
    """Levenshtein normalized by the longer string (0..1). VERBATIM from s3."""
    a, b = a.lower(), b.lower()
    if not a and not b:
        return 0.0
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return 1.0
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        ca = a[i - 1]
        for j in range(1, lb + 1):
            cost = 0 if ca == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb] / max(la, lb)


def surface_gate(src: str, para: str):
    """VERBATIM gate from iter-1 s3_surface_flips.py."""
    if not para or norm_key(para) == norm_key(src):
        return False, {"jaccard": 1.0, "char_change": 0.0, "reason": "empty_or_identical"}
    jac = token_jaccard(src, para)
    ced = norm_edit_distance(src, para)
    ok = (jac < JACCARD_MAX) and (ced > CHAR_CHANGE_MIN)
    return ok, {"jaccard": round(jac, 3), "char_change": round(ced, 3),
                "reason": "ok" if ok else "too_similar"}


REFUSAL_RE = re.compile(
    r"\b(i can('?|no)t|i cannot|i'm sorry|i am sorry|i won'?t|i will not|"
    r"as an ai|i apologi|unable to (help|assist|comply)|i must decline|"
    r"cannot (assist|help|comply|fulfil|fulfill)|against my)\b", re.I)


# ============================ model ids =========================================
GEN_MODEL = "openai/gpt-4o-mini"                 # generator (homogeneous w/ 546 originals)
JUDGE_PRIMARY = "anthropic/claude-haiku-4.5"     # independent judge (!= gpt-4o-mini, != gemini)
JUDGE_SECOND_TOX = "google/gemini-3.1-flash-lite"  # 2nd-family judge for toxicity sample
JUDGE_SECOND_FL = "deepseek/deepseek-v4-flash"   # 2nd-family judge for first-letter sample
