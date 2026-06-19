#!/usr/bin/env python3
"""Build the Homograph/Polysemy Entity Absorption Testbed.

FOUR is-a hierarchies whose surface tokens carry a strong competing NON-target sense
(exactly the competition that produces a suppressed-parent recall hole / feature absorption):

  1. city_homograph_absorption  — parent = 'is the name of a city/place'   (Phoenix, Mobile, Reading, Paris, ...)
  2. month_name_absorption       — parent = 'is a calendar month'           (May, March, August, April, June, ...)
  3. given_name_absorption       — parent = 'is a person/given name'        (Grace, Hope, Mark, Will, Rose, ...)
  4. brand_homograph_absorption  — parent = 'is a company/brand name'       (Apple, Amazon, Shell, Target, ...)

This is a STRICT structural drop-in for the iter-1 non-spelling absorption testbed
(art_t2uUbjSwpd3t): same exp_sel_data_out on-disk format, same three coordinated components
per hierarchy --
  (A) content-flip minimal pairs  (parent concept present vs absent, surface matched)
  (B) surface-flip pairs          (concept fixed, surface varied; both positive)
  (C) diagnostic corpus           (real pile-uncopyrighted windows labelled by frozen sub-context
                                   + a NEW homograph_competitor matched-negative family)
-- plus the new entity-type / neg-family enum values and per-entity homograph_strength.

NO SAE / model / activation computation here: text + labels + spans + folds only.
Sub-context / target-sense / competitor labels are assigned PURELY from surface form / regex /
gazetteer / disambiguating local context, independent of any model -- so the degenerate-construction
guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding, not baked in.
"""

from __future__ import annotations

import calendar
import re
import sys
from pathlib import Path

from loguru import logger

# ----------------------------------------------------------------------------- config / logging
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

HIERARCHIES = ["city", "month", "given_name", "brand"]
DATASET_NAME = {
    "city": "city_homograph_absorption",
    "month": "month_name_absorption",
    "given_name": "given_name_absorption",
    "brand": "brand_homograph_absorption",
}
PARENT_CONCEPT = {
    "city": "the name of a city",
    "month": "a calendar month",
    "given_name": "a person's given name",
    "brand": "a company or brand name",
}

# ----------------------------------------------------------------------------- homograph strength (wordfreq)
try:
    from wordfreq import zipf_frequency

    def homograph_strength(word: str) -> float:
        try:
            return round(float(zipf_frequency(word.lower(), "en")), 3)
        except Exception:
            return 0.0
    WORDFREQ_OK = True
except Exception as e:  # pragma: no cover - fallback path
    logger.warning(f"[wordfreq] unavailable ({repr(e)[:80]}); using neutral 'medium' tag")
    WORDFREQ_OK = False

    def homograph_strength(word: str) -> float:
        return 4.0  # neutral 'medium' tag when wordfreq missing


# ----------------------------------------------------------------------------- entity gazetteers
# Each city entity: (surface, competitor_word_lowercase, competitor_gloss, lc_is_competitor, [special_regex])
#   competitor_word_lowercase -> drives homograph_strength (Zipf of the competing common word)
#   lc_is_competitor          -> True iff a *lowercase* occurrence of the token is a reliable
#                                competitor-sense (non-target) signal in the corpus
#   special_regex             -> extra high-precision capitalised competitor cues (e.g. "Joaquin Phoenix")
CITY_RAW = [
    ("Phoenix",   "phoenix",   "mythical bird / comeback / Joaquin Phoenix", True,
     [r"Joaquin\s+Phoenix", r"(?:rose|rise|rising|risen|rises)\b.{0,25}\bashes\b"]),
    ("Mobile",    "mobile",    "adjective 'mobile' / mobile phone",          True, []),
    ("Reading",   "reading",   "gerund of 'read'",                           True, []),
    ("Bath",      "bath",      "a bathtub / bathing",                        True, []),
    ("Nice",      "nice",      "adjective 'nice' (pleasant)",                True, []),
    ("Buffalo",   "buffalo",   "the animal",                                 True, []),
    ("Hull",      "hull",      "the hull of a ship",                         True, []),
    ("Cork",      "cork",      "a bottle cork",                              True, []),
    ("Split",     "split",     "to split / a split",                         True, []),
    ("Bend",      "bend",      "to bend / a bend",                           True, []),
    ("Worth",     "worth",     "value / 'worth' preposition",                True, []),
    ("Sandy",     "sandy",     "covered in sand",                            True, []),
    ("Surprise",  "surprise",  "a surprise",                                 True, []),
    ("Cologne",   "cologne",   "perfume / eau de cologne",                   True, [r"eau\s+de\s+[Cc]ologne"]),
    ("Mercury",   "mercury",   "planet / element / Freddie Mercury",         True,
     [r"Freddie\s+Mercury", r"\bMercury\b\s+(?:is|orbits|poisoning|vapou?r|thermometer|the\s+planet)"]),
    ("Jackson",   "jackson",   "surname / Michael Jackson",                  False,
     [r"(?:Michael|Janet|Andrew|Samuel|Stonewall|Peter|Phil|Reggie|Jesse)\s+Jackson"]),
    ("Columbus",  "columbus",  "Christopher Columbus",                       False,
     [r"Christopher\s+Columbus", r"\bColumbus\s+(?:discovered|sailed|Day)\b"]),
    ("Cleveland", "cleveland", "Grover Cleveland (surname)",                 False,
     [r"(?:Grover|President)\s+Cleveland"]),
    ("Florence",  "florence",  "given name / Florence Nightingale",          False,
     [r"Florence\s+Nightingale", r"(?:Mr|Mrs|Ms|Miss|Aunt|Lady)\.?\s+Florence"]),
    ("Sydney",    "sydney",    "given name",                                 False,
     [r"(?:Mr|Mrs|Ms|Miss|Aunt)\.?\s+Sydney"]),
    ("Paris",     "paris",     "Greek myth / Paris Hilton",                  False,
     [r"Paris\s+Hilton", r"\bParis\b\s+(?:of\s+Troy|abducted|the\s+prince)"]),
    ("Jordan",    "jordan",    "the river / Michael Jordan",                 False,
     [r"Michael\s+Jordan", r"(?:River|river)\s+Jordan", r"\bJordan\s+(?:River|scored|dunked)\b"]),
    ("Hollywood", "hollywood", "the film industry",                          False,
     [r"Hollywood\s+(?:film|films|movie|movies|star|stars|studio|studios|blockbuster|actor|actress|producer|director|glamou?r|ending)"]),
]

# Months: all 12; competitor cues concentrate on the homograph-strong (May/March/August + name-months).
MONTH_NAMES = [calendar.month_name[i] for i in range(1, 13)]
MONTH_SPECIAL = {
    "May": (False, [r"\bMay\s+(?:I|we|you|he|she|it|they|the|not|have|be|or|well|come|wish|find|"
                    r"seem|cause|require|include|vary|differ|need|want|also|still|even|never|only|"
                    r"please|God|your|our|their|his|her|its|this|that|these|those|a|an)\b"]),
    "March": (True, []),    # lowercase 'march/marched/marching/marches' added below
    "August": (False, [r"\baugust\s+(?:body|bodies|assembly|presence|institution|institutions|"
                       r"gathering|personage|occasion|company|group|members?|tradition)\b"]),
    "April": (False, [r"(?:Mr|Mrs|Ms|Miss|Aunt)\.?\s+April", r"April\s+(?:O'Neil|Ludgate)"]),
    "June": (False, [r"(?:Mr|Mrs|Ms|Miss|Aunt)\.?\s+June", r"June\s+(?:Carter|Cleaver)"]),
}
MONTH_COMP_WORD = {m: m.lower() for m in MONTH_NAMES}
MONTH_COMP_GLOSS = {
    "May": "modal verb 'may'", "March": "to march / a protest march",
    "August": "adjective 'august' (distinguished)", "April": "given name",
    "June": "given name",
}

GIVEN_RAW = [  # (surface, competitor_word, gloss) -- all lc_is_competitor=True (word-names)
    ("Grace", "grace", "gracefulness / elegance"),
    ("Hope", "hope", "to hope / hope (noun)"),
    ("Faith", "faith", "religious faith"),
    ("Joy", "joy", "joy (emotion)"),
    ("Mark", "mark", "a mark / to mark"),
    ("Bill", "bill", "an invoice / a bird's beak"),
    ("Will", "will", "modal verb 'will' / a testament"),
    ("Rose", "rose", "the flower / past tense of 'rise'"),
    ("Frank", "frank", "adjective 'frank' / to frank"),
    ("Pat", "pat", "to pat"),
    ("Dawn", "dawn", "daybreak"),
    ("Summer", "summer", "the season"),
    ("Autumn", "autumn", "the season"),
    ("Crystal", "crystal", "a crystal"),
    ("Daisy", "daisy", "the flower"),
    ("Lily", "lily", "the flower"),
    ("Violet", "violet", "the flower / colour"),
    ("Ivy", "ivy", "the plant"),
    ("Holly", "holly", "the plant"),
    ("Rosemary", "rosemary", "the herb"),
    ("Pearl", "pearl", "the gem"),
    ("Ruby", "ruby", "the gem / colour"),
    ("Art", "art", "art"),
    ("Earl", "earl", "a noble rank"),
    ("Jack", "jack", "to jack / a playing card / a device"),
    ("Drew", "drew", "past tense of 'draw'"),
    ("Sky", "sky", "the sky"),
    ("Reed", "reed", "a reed (plant)"),
    ("Chase", "chase", "to chase"),
    ("Wade", "wade", "to wade"),
    ("Cliff", "cliff", "a cliff"),
    ("Dean", "dean", "an academic dean"),
    ("Robin", "robin", "the bird"),
    ("Carol", "carol", "a carol / to sing"),
]

BRAND_RAW = [  # (surface, competitor_word, gloss) -- all lc_is_competitor=True (word-brands)
    ("Apple", "apple", "the fruit"),
    ("Amazon", "amazon", "the river / rainforest / warrior"),
    ("Shell", "shell", "a seashell / a shell"),
    ("Gap", "gap", "a gap"),
    ("Dove", "dove", "the bird / past tense of 'dive'"),
    ("Target", "target", "a target / to aim at"),
    ("Orange", "orange", "the fruit / the colour"),
    ("Subway", "subway", "the underground railway"),
    ("Tide", "tide", "the ocean tide"),
    ("Corona", "corona", "a crown / the sun's corona"),
    ("Visa", "visa", "a travel visa"),
    ("Polo", "polo", "the sport"),
    ("Puma", "puma", "the animal"),
    ("Jaguar", "jaguar", "the animal"),
    ("Caterpillar", "caterpillar", "the insect"),
    ("Dawn", "dawn", "daybreak (dish-soap brand)"),
    ("Sprint", "sprint", "to sprint"),
    ("Chase", "chase", "to chase (bank brand)"),
    ("Square", "square", "a square / a town square"),
    ("Oracle", "oracle", "a prophet / an oracle"),
    ("Monster", "monster", "a monster"),
    ("Patagonia", "patagonia", "the region"),
    ("Java", "java", "the island / coffee"),
    ("Python", "python", "the snake"),
]

# Cross-hierarchy surface collisions (kept per-hierarchy with the correct target sense; noted in metadata).
COLLISIONS = {
    "Dawn": "Dawn is also a documented dish-soap BRAND (given_name vs brand)",
    "Chase": "Chase is also a documented BANK BRAND (given_name vs brand)",
    "Jordan": "Jordan is also a country (dataset_2 taxonomic); here the city/place sense is the target",
    "Mercury": "Mercury is also a planet/element (city homograph)",
    "Paris": "Paris is a homograph (myth / celebrity); city sense is the target",
}


def _build_entities():
    ents = {h: [] for h in HIERARCHIES}
    for surf, comp, gloss, lc, special in CITY_RAW:
        ents["city"].append(dict(surface=surf, target_type="city", competitor=comp,
                                 competitor_gloss=gloss, lc_is_competitor=lc,
                                 special=special, strength=homograph_strength(comp)))
    for m in MONTH_NAMES:
        lc, special = MONTH_SPECIAL.get(m, (False, []))
        comp = MONTH_COMP_WORD[m]
        gloss = MONTH_COMP_GLOSS.get(m, f"non-month sense of '{m.lower()}'")
        ents["month"].append(dict(surface=m, target_type="month", competitor=comp,
                                  competitor_gloss=gloss, lc_is_competitor=lc,
                                  special=special, strength=homograph_strength(comp)))
    for surf, comp, gloss in GIVEN_RAW:
        ents["given_name"].append(dict(surface=surf, target_type="given_name", competitor=comp,
                                       competitor_gloss=gloss, lc_is_competitor=True,
                                       special=[], strength=homograph_strength(comp)))
    for surf, comp, gloss in BRAND_RAW:
        ents["brand"].append(dict(surface=surf, target_type="brand", competitor=comp,
                                  competitor_gloss=gloss, lc_is_competitor=True,
                                  special=[], strength=homograph_strength(comp)))
    return ents


ENTITIES = _build_entities()
ENT_BY_SURFACE = {h: {e["surface"]: e for e in ENTITIES[h]} for h in HIERARCHIES}
STRENGTH = {(h, e["surface"]): e["strength"] for h in HIERARCHIES for e in ENTITIES[h]}
GLOSS = {(h, e["surface"]): e["competitor_gloss"] for h in HIERARCHIES for e in ENTITIES[h]}


# ----------------------------------------------------------------------------- geonames provenance (cities)
def annotate_city_provenance():
    """Verify each homograph-city surface is a real, populated city name (geonamescache).
    Returns {surface: {'in_geonames': bool|None, 'max_population': int}}. Provenance only; entities
    are kept regardless (they are documented homograph place names)."""
    info = {}
    try:
        import geonamescache
        gc = geonamescache.GeonamesCache(min_city_population=15000)
        cities = gc.get_cities()
        pop_by_name = {}
        for rec in cities.values():
            nm = rec.get("name")
            pop = rec.get("population", 0) or 0
            if nm:
                pop_by_name[nm] = max(pop_by_name.get(nm, 0), pop)
        for e in ENTITIES["city"]:
            s = e["surface"]
            info[s] = {"in_geonames": s in pop_by_name, "max_population": int(pop_by_name.get(s, 0))}
    except Exception as ex:  # pragma: no cover
        logger.warning(f"[geonames] unavailable ({repr(ex)[:80]}); city provenance skipped")
        for e in ENTITIES["city"]:
            info[e["surface"]] = {"in_geonames": None, "max_population": 0}
    return info


# ----------------------------------------------------------------------------- surface alternation matchers
def _alt_regex(names, ignorecase=False):
    ordered = sorted(set(names), key=len, reverse=True)
    flags = re.IGNORECASE if ignorecase else 0
    return re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(n) for n in ordered) + r")(?![A-Za-z])", flags)


# Target surfaces matched CASE-SENSITIVELY (capitalised form only).
RE_TARGET = {h: _alt_regex([e["surface"] for e in ENTITIES[h]]) for h in HIERARCHIES}

# Lowercase competitor words -> entity surface (case-SENSITIVE lowercase match).
LC_COMPETITOR_WORDS = {h: {} for h in HIERARCHIES}
for _h in HIERARCHIES:
    for _e in ENTITIES[_h]:
        if _e["lc_is_competitor"]:
            LC_COMPETITOR_WORDS[_h][_e["competitor"]] = _e["surface"]
for _w in ("march", "marched", "marching", "marches"):  # March verb inflections
    LC_COMPETITOR_WORDS["month"][_w] = "March"

RE_LC_COMP = {}
for _h in HIERARCHIES:
    _words = list(LC_COMPETITOR_WORDS[_h].keys())
    RE_LC_COMP[_h] = (re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(w) for w in
                      sorted(_words, key=len, reverse=True)) + r")(?![A-Za-z])") if _words else None)

# Special (capitalised) competitor cues: list of (surface, compiled_regex) per hierarchy.
SPECIAL_COMP = {h: [] for h in HIERARCHIES}
for _h in HIERARCHIES:
    for _e in ENTITIES[_h]:
        for _pat in _e.get("special", []):
            SPECIAL_COMP[_h].append((_e["surface"], re.compile(_pat)))


# ----------------------------------------------------------------------------- target-sense local cues
def _build_state_country():
    """Tokens that legitimately follow 'City, ' (US states + abbrevs + country first-words + UK regions).
    Used to keep the City,State cue from matching person name-lists like 'Bo Jackson, Mike LaValliere'."""
    toks = {"UK", "US", "USA", "England", "Scotland", "Wales", "Ireland", "Britain", "Yorkshire",
            "Ontario", "Quebec", "Ohio", "Texas", "California", "Florida", "Indiana", "Alabama",
            "Germany", "France", "Italy", "Canada", "Spain", "Oregon", "Australia", "Japan", "Mexico"}
    try:
        import geonamescache
        gc = geonamescache.GeonamesCache()
        for ab, rec in gc.get_us_states().items():
            toks.add(ab)
            nm = rec.get("name", "")
            if nm:
                toks.add(nm); toks.add(nm.split()[0])
        for rec in gc.get_countries().values():
            nm = rec.get("name", "")
            if nm:
                toks.add(nm.split()[0])
    except Exception:
        pass
    toks |= {"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
             "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
             "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
             "VA", "WA", "WV", "WI", "WY", "DC"}
    return toks


STATE_COUNTRY = _build_state_country()

_CITY_LEFT_PREP = re.compile(r"(?:\b(?:in|at|to|from|near|outside|downtown|visited|toured)\s+)$")
_CITY_LEFT_CITYOF = re.compile(r"\b(?:city|town)\s+of\s+$", re.IGNORECASE)
_CITY_RIGHT_STATE = re.compile(r"^,\s+([A-Z][a-zA-Z]+|[A-Z]{2})\b")
_CITY_RIGHT_SUFFIX = re.compile(r"^\s+(?:City|Airport|Station|County|metro|residents|suburb|suburbs|downtown|skyline)\b")
# After a prepositional cue, a following TitleCase word (no comma) usually means a COMPOUND proper noun
# (company/person/landmark: "Mobile Heartbeat", "Jackson Pollock"); a following common noun from this
# stoplist means the token is a MODIFIER, not a place ("Reading group", "Mobile phone", "Nice weather").
_CITY_RIGHT_TITLECASE = re.compile(r"^\s+[A-Z][a-z]+")
_CITY_RIGHT_NONPLACE = re.compile(
    r"^\s+(?:group|groups|list|lists|room|rooms|material|materials|comprehension|glasses|lamp|lamps|"
    r"age|ages|week|weeks|level|levels|club|clubs|time|times|phone|phones|app|apps|device|devices|"
    r"home|homes|banking|payment|payments|weather|day|days|guy|guys|people|work|works|festival|"
    r"library|matter|matters|skill|skills|score|scores|order|orders|number|numbers)\b")

_MONTH_LEFT_PREP = re.compile(r"(?:\b(?:in|on|since|until|by|during|early|late|mid|of)\s+)$")
_MONTH_LEFT_DEM = re.compile(r"(?:\b(?:last|next|this)\s+)$")
_MONTH_LEFT_DAY = re.compile(r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?$")
_MONTH_RIGHT_DAY = re.compile(r"^\s+\d{1,2}(?:st|nd|rd|th)?\b")
_MONTH_RIGHT_YEAR = re.compile(r"^\s+\d{4}\b")

_NAME_LEFT_TITLE = re.compile(r"(?:\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sir|Lady|President|Senator|Aunt|Uncle|Reverend|Rev|Governor|Mayor)\.?\s+)$")
_NAME_LEFT_NAMED = re.compile(r"(?:\b(?:named|called)\s+)$")
_NAME_RIGHT_TITLECASE = re.compile(r"^\s+[A-Z][a-z]+")  # a following TitleCase word -> compound proper noun (brand/org/full-name)
_NAME_RIGHT_VERB = re.compile(r"^\s+(?:said|asked|replied|smiled|nodded|wrote|added|laughed|sighed|"
                              r"whispered|shouted|agreed|recalled|grinned|frowned|shrugged|exclaimed|"
                              r"explained|muttered|insisted|continued|paused)\b")
_NAME_RIGHT_POSS = re.compile(r"^'s\s+(?:mother|father|hand|hands|face|voice|eyes|sister|brother|husband|"
                              r"wife|son|daughter|friend|parents|family|house|home|car|office|team|head|"
                              r"hair|smile|words|heart|mind|room|story|idea|decision)\b")
_NAME_RIGHT_APPOS = re.compile(r"^,\s+who\b")
# A preposition immediately before a capitalised token usually introduces a PLACE/PUBLICATION, not a
# person-subject (e.g. "writing in Dawn", "from Mercury"); block the weaker verb/appositive cues there.
_NAME_LEFT_PREP = re.compile(r"(?:\b(?:in|from|at|of|on|by|via)\s+)$")
# Given names that are ALSO a well-known org/publication (bank Chase, newspaper Dawn): for these the
# weak verb/appositive cues are unreliable ("Chase agreed to lend ...") -> require a strong person cue.
_NAME_ORG_COLLISION = {"Chase", "Dawn"}

_BRAND_RIGHT_CORP = re.compile(r"^\s*(?:Inc\b|Corp\b|Co\b|Ltd\b|LLC\b|announced|released|launched|unveiled|"
                               r"reported|shares?\b|stock\b|CEO\b|earnings|revenue|profits?\b|products?\b|"
                               r"store\b|stores\b|app\b|brand\b|company\b|customers\b)")
_BRAND_RIGHT_POSS = re.compile(r"^'s\s+(?:new|latest|CEO|stock|shares|products?|earnings|revenue|app|store|brand|market)\b")
_BRAND_LEFT_SHARES = re.compile(r"\b(?:shares?|stock|stocks|investors|analysts)\s+(?:of|in|upgraded|downgraded|rated)\s+$")
_BRAND_LEFT_PREP = re.compile(r"(?:\b(?:at|from|by|for)\s+)$")
_BRAND_RIGHT_AFTERPREP = re.compile(r"^\s+(?:Inc|Corp|store|stores|today|headquarters|HQ)\b")


def _ctx(win, s, e, nleft=24, nright=34):
    return win[max(0, s - nleft):s], win[e:e + nright]


def city_target_ok(win, s, e, surface=None):
    left, right = _ctx(win, s, e)
    # 'City, <verified state/country>' or explicit place suffix: high precision, accept outright.
    m = _CITY_RIGHT_STATE.match(right)
    if m and m.group(1) in STATE_COUNTRY:
        return True
    if _CITY_RIGHT_SUFFIX.match(right):
        return True
    # Prepositional / "city of" cue: accept only if the token is the PP head, not a modifier of a
    # following content word (rejects company/person compounds and gerund/adjective collocations).
    if _CITY_LEFT_PREP.search(left) or _CITY_LEFT_CITYOF.search(left):
        if _CITY_RIGHT_TITLECASE.match(right) or _CITY_RIGHT_NONPLACE.match(right):
            return False
        return True
    return False


def month_target_ok(win, s, e, surface=None):
    left, right = _ctx(win, s, e, nleft=18, nright=12)
    if _MONTH_LEFT_PREP.search(left) or _MONTH_LEFT_DEM.search(left) or _MONTH_LEFT_DAY.search(left):
        return True
    if _MONTH_RIGHT_DAY.match(right) or _MONTH_RIGHT_YEAR.match(right):
        return True
    return False


def name_target_ok(win, s, e, surface=None):
    left, right = _ctx(win, s, e, nleft=16, nright=24)
    if _NAME_LEFT_TITLE.search(left):  # honorific + name: very high precision
        return True
    # 'named/called X': accept unless followed by a TitleCase word (compound brand/org: "named Sky Bet").
    if _NAME_LEFT_NAMED.search(left) and not _NAME_RIGHT_TITLECASE.match(right):
        return True
    if _NAME_RIGHT_POSS.match(right):  # possessive + relation/body noun: very high precision
        return True
    if surface in _NAME_ORG_COLLISION:  # bank/newspaper collision: only the strong person cues count
        return False
    if _NAME_LEFT_PREP.search(left):    # "writing in Dawn ...": publication/place, not a person-subject
        return False
    if _NAME_RIGHT_VERB.match(right) or _NAME_RIGHT_APPOS.match(right):
        return True
    return False


def brand_target_ok(win, s, e, surface=None):
    left, right = _ctx(win, s, e, nleft=20, nright=30)
    if _BRAND_RIGHT_CORP.match(right) or _BRAND_RIGHT_POSS.match(right):
        return True
    if _BRAND_LEFT_SHARES.search(left):
        return True
    if _BRAND_LEFT_PREP.search(left) and _BRAND_RIGHT_AFTERPREP.match(right):
        return True
    return False


TARGET_OK = {"city": city_target_ok, "month": month_target_ok,
             "given_name": name_target_ok, "brand": brand_target_ok}


def detect_targets(win):
    """Return list of (hierarchy, surface, start, end) for surface matches in TARGET sense."""
    out = []
    for h in HIERARCHIES:
        for m in RE_TARGET[h].finditer(win):
            s, e = m.start(1), m.end(1)
            if TARGET_OK[h](win, s, e, m.group(1)):
                out.append((h, m.group(1), s, e))
    return out


def detect_competitors(win):
    """Return list of (hierarchy, surface, start, end) for tokens in COMPETITOR (non-target) sense."""
    out = []
    for h in HIERARCHIES:
        rc = RE_LC_COMP[h]
        if rc is not None:
            for m in rc.finditer(win):
                out.append((h, LC_COMPETITOR_WORDS[h][m.group(1)], m.start(1), m.end(1)))
        for surf, pat in SPECIAL_COMP[h]:
            mm = pat.search(win)
            if mm:
                out.append((h, surf, mm.start(), mm.end()))
    return out


def any_token(win):
    """True iff the window contains ANY target-surface OR competitor token of any hierarchy."""
    for h in HIERARCHIES:
        if RE_TARGET[h].search(win):
            return True
        if RE_LC_COMP[h] is not None and RE_LC_COMP[h].search(win):
            return True
        for _surf, pat in SPECIAL_COMP[h]:
            if pat.search(win):
                return True
    return False


# ----------------------------------------------------------------------------- templated pair frames
# Content-flip frames: (id, template, neg_family). x_on = entity (target sense, positive);
# x_off = off_filler from the matching pool (parent concept absent, negative). Surface-matched.
CONTENT_FRAMES = {
    "city": [
        ("cx1", "She flew to {S} for the conference.", "other_place"),
        ("cx2", "They drove from {S} to the airport.", "other_place"),
        ("cx3", "He grew up in {S}.", "other_place"),
        ("cx4", "The delegation arrived in {S} on Monday.", "other_place"),
        ("cx5", "Tourists rarely visit {S} in winter.", "other_place"),
        ("cx6", "We spent three days in {S}.", "other_place"),
        ("cx7", "The fastest route to {S} was closed.", "other_place"),
        ("cx8", "Heavy rain flooded {S} last night.", "other_place"),
    ],
    "month": [
        ("mx1", "The festival is scheduled for {S}.", "other_time"),
        ("mx2", "They got married in {S}.", "other_time"),
        ("mx3", "It happened back in {S} of that year.", "other_time"),
        ("mx4", "The deadline falls in early {S}.", "other_time"),
        ("mx5", "Construction will begin in {S}.", "other_time"),
        ("mx6", "Sales always peak in {S}.", "other_time"),
    ],
    "given_name": [
        ("gx1", "{S} smiled and waved at the crowd.", "other_person_ref"),
        ("gx2", "Everyone agreed that {S} was right.", "other_person_ref"),
        ("gx3", "{S} opened the door and stepped inside.", "other_person_ref"),
        ("gx4", "We waited for {S} near the entrance.", "other_person_ref"),
        ("gx5", "{S} answered every question calmly.", "other_person_ref"),
        ("gx6", "They thanked {S} for all the help.", "other_person_ref"),
    ],
    "brand": [
        ("bx1", "{S} announced a new product this morning.", "other_company_ref"),
        ("bx2", "{S} reported record earnings last quarter.", "other_company_ref"),
        ("bx3", "{S} is hiring hundreds of engineers.", "other_company_ref"),
        ("bx4", "Analysts upgraded {S} after the results.", "other_company_ref"),
        ("bx5", "{S} opened a flagship store downtown.", "other_company_ref"),
        ("bx6", "Regulators are investigating {S}.", "other_company_ref"),
    ],
}

# off-filler pools by neg_family. Each item fits ALL frames of its hierarchy and is NOT a member of
# the parent class (so x_off genuinely lacks the parent concept while staying surface-matched).
OFF_POOLS = {
    "other_place": ["France", "Japan", "Brazil", "Canada", "Norway", "Kenya", "Egypt", "Portugal",
                    "the countryside", "the mountains", "the desert", "the coast", "the suburbs",
                    "the capital", "the region", "the valley", "the highlands", "the wilderness",
                    "the province", "the border"],
    "other_time": ["spring", "summer", "winter", "autumn", "springtime", "wintertime",
                   "midsummer", "midwinter", "the offseason", "the new year", "the rainy season",
                   "the dry season"],
    "other_person_ref": ["the teacher", "the doctor", "the manager", "the stranger", "the officer",
                         "the nurse", "the driver", "the waiter", "the visitor", "the clerk",
                         "the guide", "the captain", "the lawyer", "the engineer", "our neighbor",
                         "the receptionist"],
    "other_company_ref": ["the startup", "the firm", "the company", "the retailer", "the manufacturer",
                          "the airline", "the bank", "the chain", "the vendor", "the supplier",
                          "the conglomerate", "the agency", "the carrier", "a rival"],
}

# Surface-flip frames: BOTH carriers positive (concept fixed), for the unit-level surface-invariance
# admission check. Distinct from the content frames; each forces the TARGET sense.
SURFACE_FRAMES = {
    "city": ["{S} is a remarkable place to live.", "We explored {S} on foot all weekend.",
             "The streets of {S} were crowded that evening.", "Trains to {S} run every hour.",
             "She relocated to {S} last spring.", "Travellers often pass through {S}."],
    "month": ["The festival returns every {S}.", "Their busiest period is always {S}.",
              "The semester ends in {S}.", "They always vacation during {S}.",
              "The harvest begins in {S}.", "Membership renews each {S}."],
    "given_name": ["{S} grew up in a small coastal town.", "Everyone in the office trusts {S}.",
                   "{S} has two younger siblings.", "We invited {S} to the wedding.",
                   "{S} volunteers at the shelter on weekends.", "The committee elected {S} as chair."],
    "brand": ["{S} dominates the consumer market.", "Investors remain bullish on {S} this year.",
              "{S} employs thousands of people worldwide.", "Critics praised the latest {S} release.",
              "{S} expanded aggressively into Europe.", "Loyal customers swear by {S}."],
}


# ----------------------------------------------------------------------------- row builder
def find_slot(template: str) -> int:
    return template.index("{S}")


def make_row(*, input_text, output, hierarchy, row_type, sub_context, pair_id, pair_role,
             target_text, target_char_start, target_char_end, source, pile_set_name=None,
             llm_judge_pass=None, llm_judge_score=None, fold=None, template_id=None,
             neg_family=None, entity=None, target_sense=None, competitor_sense=None,
             homograph_strength_val=None, notes=None):
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
        "metadata_entity": entity,
        "metadata_target_sense": target_sense,
        "metadata_competitor_sense": competitor_sense,
        "metadata_homograph_strength": homograph_strength_val,
        "metadata_notes": notes,
    }


def build_content_pair(*, hierarchy, entity, template, off_filler, pair_id, source, template_id,
                       neg_family, notes=None):
    """(x_on, x_off) content-flip pair; one template, surface constant within the pair."""
    slot = find_slot(template)
    x_on = template.replace("{S}", entity)
    x_off = template.replace("{S}", off_filler)
    on_start, on_end = slot, slot + len(entity)
    strength = STRENGTH.get((hierarchy, entity))
    gloss = GLOSS.get((hierarchy, entity))
    coll = COLLISIONS.get(entity)
    note_on = "; ".join([x for x in (notes, (f"collision: {coll}" if coll else None)) if x]) or None
    row_on = make_row(input_text=x_on, output="positive", hierarchy=hierarchy, row_type="content_pair",
                      sub_context=entity, pair_id=pair_id, pair_role="x_on", target_text=entity,
                      target_char_start=on_start, target_char_end=on_end, source=source,
                      template_id=template_id, neg_family=neg_family, entity=entity,
                      target_sense=hierarchy, competitor_sense=gloss, homograph_strength_val=strength,
                      notes=note_on)
    row_off = make_row(input_text=x_off, output="negative", hierarchy=hierarchy, row_type="content_pair",
                       sub_context=None, pair_id=pair_id, pair_role="x_off", target_text="",
                       target_char_start=slot, target_char_end=slot, source=source,
                       template_id=template_id, neg_family=neg_family, entity=None,
                       target_sense=None, competitor_sense=None, homograph_strength_val=None,
                       notes=f"off_filler={off_filler!r}")
    return [row_on, row_off]


def build_surface_pair(*, hierarchy, entity, frame_a, frame_b, pair_id, source, notes=None):
    """(surface_a, surface_b): same entity (target sense), two different carriers (both positive)."""
    rows = []
    strength = STRENGTH.get((hierarchy, entity))
    gloss = GLOSS.get((hierarchy, entity))
    coll = COLLISIONS.get(entity)
    note = "; ".join([x for x in (notes, (f"collision: {coll}" if coll else None)) if x]) or None
    for role, frame in (("surface_a", frame_a), ("surface_b", frame_b)):
        slot = find_slot(frame)
        text = frame.replace("{S}", entity)
        rows.append(make_row(input_text=text, output="positive", hierarchy=hierarchy,
                             row_type="surface_pair", sub_context=entity, pair_id=pair_id,
                             pair_role=role, target_text=entity, target_char_start=slot,
                             target_char_end=slot + len(entity), source=source, neg_family=None,
                             entity=entity, target_sense=hierarchy, competitor_sense=gloss,
                             homograph_strength_val=strength, notes=note))
    return rows


if __name__ == "__main__":
    prov = annotate_city_provenance()
    logger.info(f"hierarchies={HIERARCHIES}  wordfreq_ok={WORDFREQ_OK}")
    for h in HIERARCHIES:
        top = [(e["surface"], e["strength"]) for e in sorted(ENTITIES[h], key=lambda x: -x["strength"])[:6]]
        logger.info(f"{h}: {len(ENTITIES[h])} entities; top strengths={top}")
    logger.info(f"city geonames in-cache: {sum(1 for v in prov.values() if v['in_geonames'])}/{len(prov)}")
    demo = ("She flew to Phoenix in May 2019. Mr. Grace nodded. Apple announced earnings; Target shares rose. "
            "The phoenix rose from the ashes after a nice bath; he will march in spring.")
    logger.info(f"targets: {detect_targets(demo)}")
    logger.info(f"competitors: {detect_competitors(demo)}")
