#!/usr/bin/env python3
"""Build the Non-Spelling Absorption Testbed (NUMERIC primary + TAXONOMIC alternative).

Produces a TEXT-ONLY dataset for a downstream SAE feature-absorption experiment.
No SAE / model / activation computation here: text + labels + spans + folds only.

Two hierarchies, each with three coordinated components:
  (A) content-flip minimal pairs  (concept present vs absent, surface matched)
  (B) surface-flip pairs          (concept fixed, surface varied)
  (C) diagnostic corpus           (real pile-uncopyrighted windows labelled by frozen sub-context + matched negatives)

Output validates against the AII `exp_sel_data_out` schema:
  {"metadata": {...}, "datasets": [{"dataset": <name>, "examples": [{"input","output","metadata_*"}]}]}
All per-row metadata is FLATTENED into metadata_<key> keys (nested objects are not allowed by that schema).

Sub-context labels are assigned PURELY from surface form / regex / gazetteer at construction time,
independent of any model — so absorption presence/absence is an iter-2 empirical finding, not baked in.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

# ----------------------------------------------------------------------------- config
HERE = Path(__file__).resolve().parent
LOG_DIR = HERE / "logs"
LOG_DIR.mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOG_DIR / "run.log"), rotation="30 MB", level="DEBUG")

SEED = 20240617
PILE_REPO = "monology/pile-uncopyrighted"
PILE_REV = "3be90335b66f24456a5d6659d9c8d208c0357119"  # pinned commit (frozen, reproducible)
PILE_SHARDS = [f"train/{i:02d}.jsonl.zst" for i in range(30)]
LLM_MODEL = "openai/gpt-4o-mini"
LLM_PRICE_IN = 0.15e-6   # $/token
LLM_PRICE_OUT = 0.60e-6  # $/token
LLM_BUDGET_STOP = 4.0    # hard stop well under the $10 ceiling
GEMMA_TOKENIZER = "google/gemma-2-2b"

# ----------------------------------------------------------------------------- gazetteers
# Single-word, high-frequency countries (primary absorber candidates).
COUNTRIES_SINGLE = [
    "France", "Japan", "Germany", "China", "Russia", "India", "Brazil", "Mexico", "Spain",
    "Italy", "Canada", "Egypt", "Greece", "Poland", "Sweden", "Norway", "Kenya", "Portugal",
    "Argentina", "Australia", "Austria", "Belgium", "Denmark", "Finland", "Ireland", "Israel",
    "Morocco", "Nigeria", "Peru", "Thailand", "Vietnam", "Ukraine", "Switzerland", "Indonesia",
    "Iran", "Iraq", "Netherlands", "Pakistan", "Colombia", "Ethiopia",
]
# Ambiguous single-word countries (homographs); kept but flagged.
COUNTRIES_AMBIGUOUS = ["Turkey", "Chile", "Jordan", "Georgia"]
# Multi-word countries; flagged multi_token (word-piece splitting complicates them).
COUNTRIES_MULTI = [
    "United States", "Saudi Arabia", "South Korea", "New Zealand", "United Kingdom",
    "South Africa", "Costa Rica", "Sri Lanka",
]
ALL_COUNTRIES = COUNTRIES_SINGLE + COUNTRIES_AMBIGUOUS + COUNTRIES_MULTI

# Cities (matched place-negatives); none is also a country (no city-states).
CITIES = [
    "Paris", "Tokyo", "London", "Berlin", "Sydney", "Toronto", "Mumbai", "Cairo", "Madrid",
    "Rome", "Moscow", "Beijing", "Chicago", "Boston", "Vienna", "Athens", "Lisbon", "Oslo",
    "Nairobi", "Lima", "Bangkok", "Hanoi", "Dublin", "Zurich", "Jakarta", "Istanbul",
    "Shanghai", "Munich", "Barcelona", "Amsterdam", "Stockholm", "Copenhagen", "Helsinki",
    "Warsaw", "Melbourne", "Karachi", "Bogota", "Manila", "Seoul", "Houston",
]
# Other proper nouns (person / company) for the second negative family.
OTHER_ENTITIES = [
    "Mozart", "Einstein", "Shakespeare", "Picasso", "Beethoven", "Napoleon", "Darwin",
    "Newton", "Gandhi", "Lincoln", "Google", "Toyota", "Microsoft", "Samsung", "Amazon",
    "Boeing", "Ferrari", "Nokia", "Sony", "Pixar",
]

# ----------------------------------------------------------------------------- numeric regex classifier
MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|October|November|"
          r"December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)")
DATE_PATTERNS = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
    re.compile(r"\b\d{1,2}-\d{1,2}-\d{2,4}\b"),
    re.compile(rf"\b{MONTHS}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}\b"),
    re.compile(rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:of\s+)?{MONTHS}\.?\s+\d{{4}}\b"),
    re.compile(rf"\b{MONTHS}\.?\s+\d{{4}}\b"),
]
RE_PERCENT = re.compile(r"\d[\d,]*(?:\.\d+)?\s?(?:%|percent\b|percentage\b)", re.IGNORECASE)
RE_CUR_PRE = re.compile(r"[$€£¥]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|trillion|thousand|bn|m|k))?",
                        re.IGNORECASE)
RE_CUR_POST = re.compile(r"\b\d[\d,]*(?:\.\d+)?\s?(?:dollars?|euros?|USD|EUR|GBP|pounds?|yen|cents?)\b",
                         re.IGNORECASE)
RE_ORDINAL = re.compile(r"\b\d+(?:st|nd|rd|th)\b", re.IGNORECASE)
RE_COMMA = re.compile(r"\b\d{1,3}(?:,\d{3})+\b")
RE_DECIMAL = re.compile(r"\b\d+\.\d+\b")
RE_YEAR = re.compile(r"\b(?:1[5-9]\d{2}|20\d{2})\b")
RE_INT = re.compile(r"\b\d+\b")
RE_ANY_DIGIT = re.compile(r"\d")

NUMERIC_SUBS = ["year", "percent", "currency", "date", "decimal", "integer", "comma_number", "ordinal"]
PRIMARY_NUM_SUBS = ["year", "percent", "currency", "date"]


def classify_numbers(text: str):
    """Return list of (start, end, sub_context) for every number occurrence, priority-ordered.

    Priority (first claim wins): date > percent > currency > ordinal > comma_number > decimal > year > integer.
    """
    claimed = [False] * len(text)

    def is_free(s, e):
        return not any(claimed[s:e])

    def claim(s, e):
        for i in range(s, e):
            claimed[i] = True

    out = []
    stages = (
        [("date", p) for p in DATE_PATTERNS]
        + [("percent", RE_PERCENT), ("currency", RE_CUR_PRE), ("currency", RE_CUR_POST),
           ("ordinal", RE_ORDINAL), ("comma_number", RE_COMMA), ("decimal", RE_DECIMAL),
           ("year", RE_YEAR), ("integer", RE_INT)]
    )
    for sub, pat in stages:
        for m in pat.finditer(text):
            s, e = m.start(), m.end()
            if e > s and is_free(s, e):
                claim(s, e)
                out.append((s, e, sub))
    out.sort()
    return out


# ----------------------------------------------------------------------------- country / city matchers
def _alt_regex(names):
    ordered = sorted(set(names), key=len, reverse=True)  # multi-word first
    return re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(n) for n in ordered) + r")(?![A-Za-z])")


RE_COUNTRY = _alt_regex(ALL_COUNTRIES)
RE_CITY = _alt_regex(CITIES)
AMBIG_SET = set(COUNTRIES_AMBIGUOUS)
MULTI_SET = set(COUNTRIES_MULTI)


def find_countries(text):
    return [(m.group(1), m.start(1), m.end(1)) for m in RE_COUNTRY.finditer(text)]


def find_cities(text):
    return [(m.group(1), m.start(1), m.end(1)) for m in RE_CITY.finditer(text)]


# ----------------------------------------------------------------------------- templated pair data
# Each numeric frame: id, sub, template with {S}, list of on-fillers, list of off-fillers.
NUM_FRAMES = [
    # year ---------------------------------------------------------------------
    ("ny1", "year", "The treaty was signed in {S}.", ["1648", "1783", "1919", "1945", "1991"],
     ["secret", "haste", "earnest", "private"]),
    ("ny2", "year", "She was born in {S}.", ["1901", "1934", "1958", "1972", "1989"],
     ["spring", "poverty", "exile", "winter"]),
    ("ny3", "year", "The war finally ended in {S}.", ["1815", "1918", "1945", "1975", "2003"],
     ["defeat", "stalemate", "chaos", "victory"]),
    ("ny4", "year", "The company was founded in {S}.", ["1888", "1923", "1976", "1998", "2011"],
     ["secret", "earnest", "opposition", "California"]),
    ("ny5", "year", "Their first album appeared in {S}.", ["1967", "1979", "1984", "1995", "2008"],
     ["stages", "secret", "installments", "tandem"]),
    ("ny6", "year", "He retired from politics in {S}.", ["1952", "1968", "1990", "2004", "2016"],
     ["disgrace", "silence", "comfort", "style"]),
    # percent ------------------------------------------------------------------
    ("np1", "percent", "Sales rose by {S} this year.", ["12%", "27%", "5%", "8.5%", "40%"],
     ["half", "a third", "a wide margin", "double"]),
    ("np2", "percent", "Unemployment fell by {S} last quarter.", ["3%", "15%", "0.5%", "22%", "6%"],
     ["half", "a fraction", "a whisker", "a third"]),
    ("np3", "percent", "The price increased by {S} overnight.", ["10%", "33%", "150%", "2.5%", "75%"],
     ["a lot", "half", "a wide margin", "a hair"]),
    ("np4", "percent", "Turnout dropped {S} compared with last time.", ["18%", "4%", "30%", "11%", "9%"],
     ["sharply", "noticeably", "slightly", "considerably"]),
    ("np5", "percent", "Support for the measure grew by {S}.", ["20%", "45%", "7%", "60%", "3.5%"],
     ["half", "a margin", "a third", "a lot"]),
    # currency -----------------------------------------------------------------
    ("nc1", "currency", "The ticket cost {S}.", ["$240", "$15", "€50", "£99", "$1,200"],
     ["nothing", "a fortune", "plenty", "little"]),
    ("nc2", "currency", "They raised {S} for the charity.", ["$5,000", "€2,000", "$3.5 million", "£750", "$120"],
     ["millions", "nothing", "funds", "a fortune"]),
    ("nc3", "currency", "The painting sold for {S}.", ["$2 million", "€800,000", "£1,500", "$45", "¥1000"],
     ["nothing", "a fortune", "peanuts", "millions"]),
    ("nc4", "currency", "He earns {S} a month.", ["$4,200", "€3,000", "£2,500", "$900", "$15,000"],
     ["plenty", "little", "enough", "a pittance"]),
    ("nc5", "currency", "The bill came to {S}.", ["$87", "€120", "£64", "$1,050", "$9.99"],
     ["nothing", "a fortune", "more", "less"]),
    # date ---------------------------------------------------------------------
    ("nd1", "date", "The meeting is scheduled for {S}.", ["March 5, 2021", "12/25/2020", "2019-06-15",
     "January 1, 2000", "September 11, 2001"], ["Monday morning", "next week", "later", "the holidays"]),
    ("nd2", "date", "They got married on {S}.", ["June 12, 2010", "08/14/1999", "July 4, 1990",
     "5th of March 2021", "2015-09-20"], ["a whim", "Sunday", "holiday", "impulse"]),
    ("nd3", "date", "The deadline is {S}.", ["April 30, 2022", "11/01/2018", "2023-02-28",
     "October 15, 2019", "3rd of June 2020"], ["Friday", "approaching", "next month", "soon"]),
    ("nd4", "date", "The eclipse occurred on {S}.", ["08/21/2017", "July 2, 2019", "2024-04-08",
     "March 20, 2015", "1st of July 2009"], ["schedule", "cue", "time", "Tuesday"]),
    # decimal ------------------------------------------------------------------
    ("ndc1", "decimal", "The sensor reading was {S}.", ["3.14", "0.05", "2.718", "7.25", "0.99"],
     ["normal", "stable", "erratic", "high"]),
    ("ndc2", "decimal", "The average score came out to {S}.", ["7.5", "4.2", "8.75", "6.0", "3.33"],
     ["high", "low", "average", "mixed"]),
    ("ndc3", "decimal", "The solution measured {S} on the scale.", ["1.5", "9.1", "0.001", "5.5", "12.4"],
     ["normal", "neutral", "high", "off"]),
    # integer ------------------------------------------------------------------
    ("ni1", "integer", "She bought {S} apples at the market.", ["47", "3", "12", "250", "8"],
     ["several", "many", "a few", "fresh"]),
    ("ni2", "integer", "There were {S} people in the room.", ["19", "64", "7", "128", "30"],
     ["several", "many", "few", "countless"]),
    ("ni3", "integer", "He scored {S} points in the game.", ["21", "5", "100", "42", "16"],
     ["plenty", "several", "many", "few"]),
    ("ni4", "integer", "The team has {S} active members.", ["11", "25", "6", "40", "9"],
     ["several", "many", "few", "new"]),
    # comma_number -------------------------------------------------------------
    ("ncm1", "comma_number", "The city has a population of {S}.", ["1,000,000", "250,000", "45,000",
     "3,200,000", "12,500"], ["millions", "thousands", "many", "few"]),
    ("ncm2", "comma_number", "The stadium holds {S} fans.", ["45,000", "82,500", "12,345", "60,000",
     "1,024"], ["thousands", "many", "countless", "crowds"]),
    ("ncm3", "comma_number", "They sold {S} copies in a week.", ["1,250,000", "330,000", "78,900",
     "2,000,000", "9,500"], ["millions", "thousands", "plenty", "few"]),
    # ordinal ------------------------------------------------------------------
    ("no1", "ordinal", "She finished in {S} place.", ["2nd", "3rd", "5th", "21st", "10th"],
     ["last", "good", "poor", "record"]),
    ("no2", "ordinal", "This is the {S} time it has happened.", ["21st", "42nd", "100th", "3rd", "7th"],
     ["last", "final", "same", "umpteenth"]),
    ("no3", "ordinal", "They celebrated their {S} anniversary.", ["25th", "42nd", "50th", "1st", "10th"],
     ["last", "silver", "golden", "final"]),
]

# Taxonomic content frames: id, template, negative family ("city" | "other").
TAX_FRAMES = [
    ("tx1", "She flew to {S} for the summit.", "city"),
    ("tx2", "He has always wanted to visit {S}.", "city"),
    ("tx3", "The delegation from {S} arrived early.", "city"),
    ("tx4", "{S} signed the trade agreement yesterday.", "city"),
    ("tx5", "He admired {S} above all others.", "other"),
    ("tx6", "Imports from {S} have risen sharply.", "city"),
    ("tx7", "The team proudly represented {S} at the games.", "city"),
    ("tx8", "She wrote her thesis on the history of {S}.", "city"),
    ("tx9", "Few tourists ever travel to {S} in winter.", "city"),
    ("tx10", "The article compared {S} with its neighbours.", "other"),
]

# Surface-flip carrier frames (the concept token is embedded; concept stays present).
NUM_SURFACE_FRAMES = {
    "year": ["In {S}, everything changed for the family.", "The group disbanded back in {S}.",
             "Nobody expected what happened in {S}.", "It was not until {S} that they met again."],
    "percent": ["Margins improved by {S} over the period.", "A gain of {S} surprised the analysts.",
                "The index closed {S} higher today.", "Costs were cut by {S} across the board."],
    "currency": ["The deal was worth {S} in total.", "She paid {S} without hesitation.",
                 "A sum of {S} was transferred overnight.", "It fetched {S} at the auction."],
    "date": ["Everything was finalised on {S}.", "The ceremony took place on {S}.",
             "We will reconvene on {S}.", "Records show it began on {S}."],
    "decimal": ["The instrument settled at {S}.", "A value of {S} was recorded.",
                "Readings hovered around {S} all day.", "The coefficient was estimated at {S}."],
    "integer": ["Altogether there were {S} of them.", "The crate held {S} in total.",
                "A group of {S} set out at dawn.", "They counted {S} before stopping."],
    "comma_number": ["The ledger listed {S} entries.", "Attendance reached {S} that night.",
                     "A total of {S} was confirmed.", "The archive held {S} files."],
    "ordinal": ["It was their {S} attempt overall.", "She placed {S} once again.",
                "This marks the {S} occasion.", "He came {S} in the final standings."],
}
TAX_SURFACE_FRAMES = [
    "{S} exports a great deal of machinery.", "Many travellers dream of seeing {S}.",
    "The economy of {S} grew last year.", "Historians have long studied {S}.",
    "Cars from {S} dominate the market.", "The cuisine of {S} is famous worldwide.",
]
NUM_SURFACE_VALUES = {
    "year": ["1989", "2001", "1969", "1945", "2012"],
    "percent": ["12%", "27%", "5%", "40%", "8.5%"],
    "currency": ["$240", "$1,200", "€50", "£99", "$3.5 million"],
    "date": ["March 5, 2021", "12/25/2020", "2019-06-15", "January 1, 2000", "July 4, 1990"],
    "decimal": ["3.14", "0.05", "7.25", "2.718", "9.1"],
    "integer": ["47", "12", "250", "64", "8"],
    "comma_number": ["1,000,000", "45,000", "250,000", "12,345", "82,500"],
    "ordinal": ["2nd", "3rd", "21st", "42nd", "10th"],
}


# ----------------------------------------------------------------------------- row builder
def find_slot(template: str) -> int:
    return template.index("{S}")


def make_row(*, input_text, output, hierarchy, row_type, sub_context, pair_id, pair_role,
             target_text, target_char_start, target_char_end, source, pile_set_name=None,
             llm_judge_pass=None, llm_judge_score=None, fold=None, template_id=None,
             neg_family=None, multi_token=False, notes=None):
    return {
        "input": input_text,
        "output": output,
        "metadata_hierarchy": hierarchy,
        "metadata_row_type": row_type,
        "metadata_concept_present": (output == "positive"),
        "metadata_sub_context": sub_context,
        "metadata_pair_id": pair_id,
        "metadata_pair_role": pair_role,
        "metadata_target_text": target_text,
        "metadata_target_char_start": target_char_start,
        "metadata_target_char_end": target_char_end,
        "metadata_target_token_indices": None,  # filled in tokenization pass
        "metadata_source": source,
        "metadata_pile_set_name": pile_set_name,
        "metadata_llm_judge_pass": llm_judge_pass,
        "metadata_llm_judge_score": llm_judge_score,
        "metadata_fold": fold,
        "metadata_template_id": template_id,
        "metadata_neg_family": neg_family,
        "metadata_multi_token": multi_token,
        "metadata_notes": notes,
    }


def build_content_pair(*, hierarchy, sub_context, template, on_filler, off_filler, pair_id,
                       source, template_id, neg_family=None, multi_token=False, notes=None):
    """Build an (x_on, x_off) content-flip pair sharing one template (surface constant within pair)."""
    slot = find_slot(template)
    x_on = template.replace("{S}", on_filler)
    x_off = template.replace("{S}", off_filler)
    on_start, on_end = slot, slot + len(on_filler)
    off_start = slot  # the differing word position in x_off
    row_on = make_row(input_text=x_on, output="positive", hierarchy=hierarchy, row_type="content_pair",
                      sub_context=sub_context, pair_id=pair_id, pair_role="x_on", target_text=on_filler,
                      target_char_start=on_start, target_char_end=on_end, source=source,
                      template_id=template_id, neg_family=neg_family, multi_token=multi_token,
                      notes=notes)
    row_off = make_row(input_text=x_off, output="negative", hierarchy=hierarchy, row_type="content_pair",
                       sub_context=None, pair_id=pair_id, pair_role="x_off", target_text="",
                       target_char_start=off_start, target_char_end=off_start, source=source,
                       template_id=template_id, neg_family=neg_family, multi_token=multi_token,
                       notes=f"off_filler={off_filler!r}" + (f"; {notes}" if notes else ""))
    return [row_on, row_off]


def build_surface_pair(*, hierarchy, sub_context, frame_a, frame_b, value, pair_id, source,
                       multi_token=False, notes=None):
    """Build a (surface_a, surface_b) pair: same concept token, two different carriers (both positive)."""
    rows = []
    for role, frame in (("surface_a", frame_a), ("surface_b", frame_b)):
        slot = find_slot(frame)
        text = frame.replace("{S}", value)
        rows.append(make_row(input_text=text, output="positive", hierarchy=hierarchy,
                             row_type="surface_pair", sub_context=sub_context, pair_id=pair_id,
                             pair_role=role, target_text=value, target_char_start=slot,
                             target_char_end=slot + len(value), source=source, multi_token=multi_token,
                             notes=notes))
    return rows
