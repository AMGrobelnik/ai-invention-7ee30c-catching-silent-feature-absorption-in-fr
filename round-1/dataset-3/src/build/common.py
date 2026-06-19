"""Shared helpers for the Two-Track CCRG toxicity dataset family build.

All cross-component invariants (text normalization, stable hashing, fold
assignment, the six civil_comments sub-attributes, the shared row schema)
live here so every stage emits byte-compatible records.
"""
from __future__ import annotations

import hashlib
import logging
import re
import sys

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                         datefmt="%H:%M:%S"))
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# The six civil_comments sub-attributes (excludes the overall `toxicity` axis,
# which is the binary task label, not a sub-context).
SUB_ATTRS = [
    "severe_toxicity",
    "obscene",
    "threat",
    "insult",
    "identity_attack",
    "sexual_explicit",
]

# All float axes preserved (toxicity + the six sub-attributes).
FLOAT_AXES = ["toxicity"] + SUB_ATTRS

PRIMARY_THRESHOLD = 0.5      # pre-registered binary threshold
FALLBACK_THRESHOLD = 0.3     # pre-registered relaxation for rare sub-contexts
CLEAN_NEG_CEILING = 0.2      # toxicity < this => clean non-toxic negative
N_MIN = 150                  # minimum positives per sub-context for the MDE

FOLDS = ("train", "val", "test")

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]", flags=re.UNICODE)
_HTML_ENT = re.compile(r"&(amp|lt|gt|quot|#39|nbsp|apos);")
_HTML_ENT_MAP = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
                 "&#39;": "'", "&nbsp;": " ", "&apos;": "'"}


# ---------------------------------------------------------------------------
# Text cleaning + hashing
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Light cleaning: unescape common HTML entities and normalize whitespace.

    Preserves the surface form (casing, punctuation, profanity) — only fixes
    markup and whitespace so the toxic signal is untouched.
    """
    if text is None:
        return ""
    t = _HTML_ENT.sub(lambda m: _HTML_ENT_MAP.get(m.group(0), m.group(0)), str(text))
    t = t.replace(" ", " ").replace("\r", " ").replace("\n", " ")
    t = _WS.sub(" ", t).strip()
    return t


def norm_key(text: str) -> str:
    """Aggressive normalization used ONLY for de-duplication / collision keys:
    lowercase, strip punctuation, collapse whitespace."""
    t = clean_text(text).lower()
    t = _PUNCT.sub(" ", t)
    t = _WS.sub(" ", t).strip()
    return t


def sha16(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def source_sentence_id(toxic_text: str) -> str:
    """Stable id grouping all paraphrases / pair-members of one source toxic
    sentence (computed from the normalized key so trivial surface variants of
    the same source collapse together for fold assignment)."""
    return "ssid_" + sha16(norm_key(toxic_text))


def fold_from_ssid(ssid: str, ratios=(0.8, 0.1, 0.1)) -> str:
    """Deterministic, leakage-safe fold from a stable bucket of the ssid hash.
    All members sharing an ssid therefore land in the SAME fold."""
    bucket = int(hashlib.sha1(ssid.encode("utf-8")).hexdigest(), 16) % 1000
    train_cut = int(ratios[0] * 1000)
    val_cut = train_cut + int(ratios[1] * 1000)
    if bucket < train_cut:
        return "train"
    if bucket < val_cut:
        return "val"
    return "test"


# ---------------------------------------------------------------------------
# Shared row schema
# ---------------------------------------------------------------------------

def make_row(
    *,
    rid: str,
    input_text: str,
    output_label: str,
    fold: str,
    record_type: str,
    source: str,
    toxicity_label: int,
    text_on=None,
    text_off=None,
    text_paired=None,
    pair_id=None,
    ssid=None,
    is_content_pair: bool = False,
    is_surface_pair: bool = False,
    subcontext_labels=None,
    subcontext_floats=None,
    subcontext_threshold=None,
    judge_pass=None,
    gen_model=None,
) -> dict:
    """Build ONE example row in the shared schema.

    Conforms to the `exp_sel_data_out` JSON schema: only `input`, `output`,
    and `metadata_*` keys are permitted on an example, so every domain field
    is carried under a `metadata_` prefix.
    """
    if subcontext_labels is None:
        subcontext_labels = {a: None for a in SUB_ATTRS}
    if subcontext_floats is None:
        subcontext_floats = {a: None for a in FLOAT_AXES}
    return {
        "input": input_text,
        "output": output_label,
        "metadata_id": rid,
        "metadata_fold": fold,
        "metadata_record_type": record_type,
        "metadata_source": source,
        "metadata_toxicity_label": int(toxicity_label),
        "metadata_text_on": text_on,
        "metadata_text_off": text_off,
        "metadata_text_paired": text_paired,
        "metadata_pair_id": pair_id,
        "metadata_source_sentence_id": ssid,
        "metadata_is_content_pair": bool(is_content_pair),
        "metadata_is_surface_pair": bool(is_surface_pair),
        "metadata_subcontext_labels": subcontext_labels,
        "metadata_subcontext_floats": subcontext_floats,
        "metadata_subcontext_threshold": subcontext_threshold,
        "metadata_judge_pass": judge_pass,
        "metadata_gen_model": gen_model,
    }
