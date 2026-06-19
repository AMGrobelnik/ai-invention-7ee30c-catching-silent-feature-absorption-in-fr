#!/usr/bin/env python3
"""Build the Safety-Relevant Identity Absorption Testbed (M2' building block).

FOUR safety-relevant is-a / identity hierarchies whose surface tokens frequently carry a strong
competing NON-identity sense (the same polysemy that produced the Georgia-homograph suppressed-parent
recall hole in the iter-1 taxonomic testbed):

  1. nationality_absorption        — parent = 'a nationality / demonym'      (American, Polish, Chinese, ...)
  2. religion_absorption           — parent = 'a religion / religious group'  (Muslim, Christian, Catholic, ...)
  3. ethnicity_identity_absorption — parent = 'a race / ethnicity / identity' (Black, White, Asian, Latino, Jewish, ...)
  4. named_entity_safety           — parent = 'a public figure / organization'(Apple, Bush, Swift, Amazon, ...)

This is a STRICT structural drop-in for the iter-1 non-spelling absorption testbed (gen_art_dataset_2)
and the iter-5 homograph/polysemy testbed (gen_art_dataset_1): same exp_sel_data_out on-disk format,
same three coordinated components per hierarchy --
  (A) content-flip minimal pairs  (identity token present vs a surface-matched non-identity word, both
                                   otherwise identical; x_on positive / x_off negative)
  (B) surface-flip pairs          (identity token fixed, carrier varied; both positive) for the
                                   unit-level surface-invariance admission
  (C) diagnostic corpus           (real pile-uncopyrighted windows labelled by frozen surface-derived
                                   sub-context, PLUS a homograph_distractor matched-negative family --
                                   the SAME token in its competing NON-identity sense -- and easy
                                   no-identity negatives)
-- plus the safety-relevant hierarchy / neg-family enum values, parent_concept, homograph_sense and a
homograph competitor gloss.

NO SAE / model / activation computation here: text + labels + spans + folds only.  sub_context /
target-sense / competitor labels are assigned PURELY from surface form / gazetteer / high-precision
disambiguating local context, independent of any model -- so the degenerate-construction guard holds
and absorption presence/absence stays a future-iteration EMPIRICAL finding, NOT baked in.  The same
labelled corpus equally supports the honest 'no safety attribute is absorption-structured' null
(uniform high parent recall) and a positive finding (sub-context-specific parent holes).
"""

from __future__ import annotations

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
# optional safety-relevant identity-rich supplement (CC0); Pile is the guaranteed fallback
CIVIL_REPO = "google/civil_comments"
GEN_MODEL = "openai/gpt-4o-mini"        # generator (templated backbone carries most rows)
JUDGE_MODEL = "anthropic/claude-haiku-4.5"  # independent judge (DIFFERENT family than generator)
GEN_PRICE_IN, GEN_PRICE_OUT = 0.15e-6, 0.60e-6      # $/token (gpt-4o-mini)
JUDGE_PRICE_IN, JUDGE_PRICE_OUT = 1.00e-6, 5.00e-6  # $/token (claude-haiku-4.5)
LLM_BUDGET_STOP = 4.0   # hard stop well under the $10 ceiling
GEMMA_TOKENIZER = "google/gemma-2-2b"

HIERARCHIES = ["nationality", "religion", "ethnicity_identity", "named_entity_safety"]
DATASET_NAME = {
    "nationality": "nationality_absorption",
    "religion": "religion_absorption",
    "ethnicity_identity": "ethnicity_identity_absorption",
    "named_entity_safety": "named_entity_safety",
}
PARENT_CONCEPT = {
    "nationality": "a nationality / demonym (a word naming the people of a country)",
    "religion": "a religion or religious-identity group",
    "ethnicity_identity": "a race / ethnicity / identity-group",
    "named_entity_safety": "a named public figure or organization",
}
# short concept phrase used in LLM judge prompts
JUDGE_CONCEPT = {
    "nationality": "a nationality / demonym (naming the people of a country)",
    "religion": "a religion or religious-identity group",
    "ethnicity_identity": "a race / ethnicity / identity-group mention",
    "named_entity_safety": "a named public figure or organization",
}
SAFETY_RELEVANT = True


# ----------------------------------------------------------------------------- homograph strength (wordfreq)
try:
    from wordfreq import zipf_frequency

    def homograph_strength(word) -> float:
        if not word:
            return None
        try:
            return round(float(zipf_frequency(str(word).lower(), "en")), 3)
        except Exception:
            return 0.0
    WORDFREQ_OK = True
except Exception as e:  # pragma: no cover - fallback
    logger.warning(f"[wordfreq] unavailable ({repr(e)[:80]}); homograph_strength=None")
    WORDFREQ_OK = False

    def homograph_strength(word):
        return None


# ----------------------------------------------------------------------------- entity gazetteers
def E(surface, *, variants=None, homograph=False, competitor=None, gloss=None, excl=None,
      lc_comp=None, meta=None):
    """One identity entity. surface=canonical token; variants=extra surface forms mapped to the same
    sub_context; homograph=has a dominant non-identity sense; competitor/gloss describe that sense;
    excl=regexes that, matching the local context of an occurrence, mark it as the COMPETING sense;
    lc_comp=lowercase competitor words detected as homograph_distractor negatives; meta=free notes."""
    return dict(surface=surface, variants=list(variants or []), homograph=homograph,
                competitor=competitor, gloss=gloss, excl=list(excl or []),
                lc_comp=list(lc_comp or []), meta=meta,
                strength=homograph_strength(competitor) if homograph else None)


# --- (1) NATIONALITY: demonyms; prioritise homographs with a dominant non-nationality sense ----------
NAT_ENTITIES = [
    # homographs (dominant NON-nationality sense)
    E("Polish", variants=[], homograph=True, competitor="polish",
      gloss="to polish / nail polish (verb/noun 'polish')",
      lc_comp=["polish", "polished", "polishing", "polishes"],
      excl=[r"\b[Pp]olish\s+(?:the|her|his|my|your|its|their|off|up|nails?|shoes?|silver|"
            r"furniture|wood|floors?|surfaces?|boots?|brass|leather)\b",
            r"\b(?:nail|shoe|furniture|silver|french|spit|metal|wood|boot)\s+polish\b"]),
    E("Dutch", variants=[], homograph=True, competitor="dutch",
      gloss="Dutch oven / go Dutch / Dutch courage",
      lc_comp=[],
      excl=[r"\b[Dd]utch\s+(?:oven|ovens|courage|uncle|door|doors|auction|angle|tilt|cap|baby)\b",
            r"\b(?:go|going|went|gone|paying|pay|split|splitting)\s+[Dd]utch\b"]),
    E("Turkish", variants=[], homograph=True, competitor="turkish",
      gloss="Turkish bath / Turkish delight / Turkish coffee",
      excl=[r"\bTurkish\s+(?:delight|bath|baths|coffee|towel|towels|angora|tobacco|van)\b"]),
    E("Indian", variants=["Indians"], homograph=True, competitor="indian",
      gloss="Native American / Indian summer / Indian Ocean",
      excl=[r"\bIndian\s+(?:summer|ink|corn|file|club|clubs|elephant|elephants|Ocean|reservation|"
            r"reservations|tribe|tribes|chief|chiefs|nation|nations|burial|reserve|Territory|giver|"
            r"paintbrush|wedding|run|trail|head|takeaway|takeout)\b",
            r"\b(?:American|Native|Red)\s+Indians?\b",
            r"\b(?:Cleveland|Atlanta)\s+Indians\b"]),
    E("Greek", variants=[], homograph=True, competitor="greek",
      gloss="Greek letters / Greek myth / Greek yogurt",
      excl=[r"\b(?:it'?s|all)\s+Greek\b",
            r"\bGreek\s+(?:letter|letters|alphabet|life|system|god|gods|goddess|goddesses|mythology|"
            r"myth|myths|yogurt|yoghurt|salad|column|columns|fraternity|sorority|key|cross|fire|"
            r"chorus|tragedy)\b"]),
    E("Cuban", variants=["Cubans"], homograph=True, competitor="cuban",
      gloss="Cuban cigar / Cuban heel / Cuban sandwich",
      excl=[r"\bCuban\s+(?:cigar|cigars|heel|heels|sandwich|sandwiches|link|links|chain|missile)\b"]),
    # high-frequency CLEAN demonyms (will easily clear the 150 diagnostic-positive bar)
    E("American", variants=["Americans"]),
    E("Russian", variants=["Russians"]),
    E("Chinese"),
    E("German", variants=["Germans"]),
    E("French"),
    E("Japanese"),
    E("Mexican", variants=["Mexicans"]),
    E("Italian", variants=["Italians"]),
    E("Spanish"),
    E("British"),
    E("Canadian", variants=["Canadians"]),
    E("Australian", variants=["Australians"]),
    E("Brazilian", variants=["Brazilians"]),
    E("Nigerian", variants=["Nigerians"]),
    E("Egyptian", variants=["Egyptians"]),
    E("Korean", variants=["Koreans"]),
    E("Iranian", variants=["Iranians"]),
    E("Pakistani", variants=["Pakistanis"]),
    E("Vietnamese"),
    E("Irish"),
    E("Israeli", variants=["Israelis"]),
    E("Ukrainian", variants=["Ukrainians"]),
    E("Filipino", variants=["Filipinos"]),
    E("Swedish"),
    E("Norwegian", variants=["Norwegians"]),
]

# --- (2) RELIGION: religious-identity tokens -----------------------------------------------------------
REL_ENTITIES = [
    # homographs
    E("Christian", variants=["Christians"], homograph=True, competitor="Christian (given name)",
      gloss="a person's given name (e.g. Christian Bale); 'Christian name' = first name",
      excl=[r"\b(?:Hans\s+)?Christian\s+(?:Bale|Andersen|Dior|Slater|Grey|Louboutin|McBride|Eriksen|"
            r"Pulisic|Aguilera|Wolff|Doppler|Barnard|Ronaldo|name)\b",
            r"\b(?:Mr|Mrs|Ms|Dr|Saint|St)\.?\s+Christian\b",
            r"\b(?:named|called)\s+Christian\b"]),
    E("Catholic", variants=["Catholics"], homograph=True, competitor="catholic",
      gloss="lowercase 'catholic' = universal / broad / wide-ranging",
      lc_comp=[],
      excl=[r"\bcatholic\s+(?:tastes?|taste|interests?|appeal|view|views|sensibilit(?:y|ies)|"
            r"selection|range|outlook)\b"]),
    # clean religious identities
    E("Muslim", variants=["Muslims"]),
    E("Hindu", variants=["Hindus"]),
    E("Buddhist", variants=["Buddhists"]),
    E("Sikh", variants=["Sikhs"]),
    E("Mormon", variants=["Mormons"]),
    E("Protestant", variants=["Protestants"]),
    E("Methodist", variants=["Methodists"]),
    E("Baptist", variants=["Baptists"]),
    E("Evangelical", variants=["Evangelicals"]),
    E("Atheist", variants=["Atheists"]),
]

# --- (3) ETHNICITY / IDENTITY: strongest homographs Black / White (Georgia-style polysemy) ------------
ETH_ENTITIES = [
    E("Black", variants=["Blacks"], homograph=True, competitor="black",
      gloss="the colour black / dark (black car, Black Sea, black hole, Black Friday)",
      excl=[r"\b[Bb]lack\s+(?:Sea|Friday|hole|holes|box|boxes|market|markets|magic|belt|belts|Death|"
            r"smith|smiths|berry|berries|bird|birds|board|boards|list|lists|gold|metal|tea|coffee|"
            r"pepper|widow|swan|ops|water|powder|ice|spot|currant|jack|Hawk|Mirror|Panther|out|"
            r"car|cars|dress|dresses|coat|coats|shirt|shirts|hair|paint|ink|dog|cat|horse|leather|"
            r"suit|suits|shoes?|screen|background|smoke|clouds?|night|sky|colou?r|hat|hats|gown)\b",
            r"\b(?:jet|pitch|coal|ink)[\s-]black\b"]),
    E("White", variants=["Whites"], homograph=True, competitor="white",
      gloss="the colour white / White House (white car, white wine, white noise)",
      excl=[r"\b[Ww]hite\s+(?:House|Sea|noise|wine|bread|board|boards|paper|papers|space|out|wash|"
            r"washing|smith|smiths|head|heads|cap|caps|tail|fish|gold|lie|lies|flag|flags|knight|"
            r"hat|hats|Christmas|Walker|Stripes|Album|sauce|rice|car|cars|dress|dresses|shirt|"
            r"shirts|paint|wall|walls|hair|snow|clouds?|coat|coats|background|screen|colou?r|"
            r"powder|light|gloves|sand|teeth|blood|cell|cells|matter|meat)\b"]),
    E("Asian", variants=["Asians"], homograph=True, competitor="asian",
      gloss="geographic adjective 'Asian' (Asian markets, Asian cuisine, Asian countries)",
      excl=[r"\bAsian\s+(?:countries|country|markets?|economies|economy|cuisines?|food|carp|elephants?|"
            r"nations?|continent|region|regions|tour|currenc(?:y|ies)|stocks?|games|Games|languages?|"
            r"art|flush|tiger|tigers|giant|giants|pear|pears|noodles?)\b"]),
    E("Native", variants=[], homograph=True, competitor="native",
      gloss="native speaker / native plant / 'native to' (the default/innate sense)",
      excl=[r"\bnative\s+(?:speakers?|plants?|species|tongue|languages?|apps?|advertising|format|"
            r"son|land|lands|habitat|range|vegetation|grasses?|trees?|wildlife|flora|fauna)\b",
            r"\b(?:a|the|is|are|was|were)\s+native\s+(?:of|to)\b"]),
    # clean identities
    E("Latino", variants=["Latinos"]),
    E("Latina", variants=["Latinas"]),
    E("Hispanic", variants=["Hispanics"]),
    E("Indigenous"),
    E("Arab", variants=["Arabs"]),
    E("Jewish", variants=["Jews"],
      meta="dual-membership: 'Jewish' is BOTH a religion and an ethnicity; canonical owner here = "
           "ethnicity_identity (kept OUT of the religion hierarchy to avoid cross-dataset duplicates)"),
    E("African American", variants=["African Americans", "African-American", "African-Americans"]),
]

# --- (4) NAMED ENTITY (safety): public figures / orgs that are also common words ----------------------
NE_ENTITIES = [
    # organisations that are common words
    E("Apple", homograph=True, competitor="apple", gloss="the fruit", lc_comp=["apple", "apples"]),
    E("Amazon", homograph=True, competitor="amazon", gloss="the river / rainforest / warrior",
      lc_comp=["amazon"]),
    E("Shell", homograph=True, competitor="shell", gloss="a seashell / a shell", lc_comp=["shell", "shells"]),
    E("Target", homograph=True, competitor="target", gloss="a target / to aim at", lc_comp=["target", "targets"]),
    E("Oracle", homograph=True, competitor="oracle", gloss="a prophet / an oracle", lc_comp=["oracle"]),
    E("Visa", homograph=True, competitor="visa", gloss="a travel visa", lc_comp=["visa", "visas"]),
    E("Corona", homograph=True, competitor="corona", gloss="a crown / the sun's corona", lc_comp=["corona"]),
    E("Subway", homograph=True, competitor="subway", gloss="the underground railway", lc_comp=["subway"]),
    E("Gap", homograph=True, competitor="gap", gloss="a gap", lc_comp=["gap", "gaps"]),
    E("Monster", homograph=True, competitor="monster", gloss="a monster", lc_comp=["monster", "monsters"]),
    E("Tide", homograph=True, competitor="tide", gloss="the ocean tide", lc_comp=["tide", "tides"]),
    # public figures whose surname is a common word
    E("Bush", homograph=True, competitor="bush", gloss="a shrub / the bush", lc_comp=["bush", "bushes"]),
    E("Cash", homograph=True, competitor="cash", gloss="money / to cash", lc_comp=["cash"]),
    E("Stone", homograph=True, competitor="stone", gloss="a rock / a stone", lc_comp=["stone", "stones"]),
    E("Banks", homograph=True, competitor="banks", gloss="riverbanks / financial banks", lc_comp=["banks"]),
    E("West", homograph=True, competitor="west", gloss="the compass direction west", lc_comp=["west"]),
    E("Swift", homograph=True, competitor="swift", gloss="fast / the bird swift", lc_comp=["swift"]),
    E("Gates", homograph=True, competitor="gates", gloss="gates (a barrier)", lc_comp=["gates"]),
    E("Cook", homograph=True, competitor="cook", gloss="to cook / a cook", lc_comp=["cook", "cooks"]),
    E("Page", homograph=True, competitor="page", gloss="a page", lc_comp=["page", "pages"]),
    E("Bell", homograph=True, competitor="bell", gloss="a bell", lc_comp=["bell", "bells"]),
    E("King", homograph=True, competitor="king", gloss="a monarch / a king", lc_comp=["king", "kings"]),
    E("Fox", homograph=True, competitor="fox", gloss="the animal fox", lc_comp=["fox", "foxes"]),
    E("Snow", homograph=True, competitor="snow", gloss="snow", lc_comp=["snow"]),
    E("Pope", homograph=True, competitor="pope", gloss="the pope (title)", lc_comp=["pope", "popes"]),
    E("Hunt", homograph=True, competitor="hunt", gloss="to hunt / a hunt", lc_comp=["hunt", "hunts"]),
    E("Wood", homograph=True, competitor="wood", gloss="wood", lc_comp=["wood", "woods"]),
    E("Bird", homograph=True, competitor="bird", gloss="a bird", lc_comp=["bird", "birds"]),
    E("Diamond", homograph=True, competitor="diamond", gloss="a diamond (gem)", lc_comp=["diamond", "diamonds"]),
]

ENTITIES = {
    "nationality": NAT_ENTITIES,
    "religion": REL_ENTITIES,
    "ethnicity_identity": ETH_ENTITIES,
    "named_entity_safety": NE_ENTITIES,
}
# whether each hierarchy's target surfaces are matched case-insensitively (Black/White/etc are
# frequently lowercase in real identity mentions: "black voters", "white families")
IGNORECASE_H = {"nationality": False, "religion": False,
                "ethnicity_identity": True, "named_entity_safety": False}

# canonical sub_context per surface variant; gloss / strength / homograph lookups
SURFACE_TO_CANON = {h: {} for h in HIERARCHIES}
ENT_BY_CANON = {h: {} for h in HIERARCHIES}
for _h in HIERARCHIES:
    for _e in ENTITIES[_h]:
        ENT_BY_CANON[_h][_e["surface"]] = _e
        for _s in [_e["surface"], *_e["variants"]]:
            SURFACE_TO_CANON[_h][_s] = _e["surface"]

GLOSS = {(h, e["surface"]): e["gloss"] for h in HIERARCHIES for e in ENTITIES[h]}
STRENGTH = {(h, e["surface"]): e["strength"] for h in HIERARCHIES for e in ENTITIES[h]}
HOMOGRAPH = {(h, e["surface"]): e["homograph"] for h in HIERARCHIES for e in ENTITIES[h]}

# cross-hierarchy / dual-membership collision notes
COLLISIONS = {
    "Jewish": "dual identity: religion AND ethnicity; canonical owner = ethnicity_identity here",
    "Indian": "homograph: India-nationality vs Native-American 'Indian' vs Indian Ocean/summer",
    "Arab": "Arab is an ethnicity here; many Arabs are also Muslim (religion) — kept separate",
}


# ----------------------------------------------------------------------------- regex compilation
def _alt_regex(names, ignorecase=False):
    ordered = sorted(set(names), key=len, reverse=True)
    flags = re.IGNORECASE if ignorecase else 0
    return re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(n) for n in ordered) + r")(?![A-Za-z])", flags)


# target-surface matchers (per hierarchy, case per IGNORECASE_H); include all variants
RE_TARGET = {}
for _h in HIERARCHIES:
    _surfs = [s for e in ENTITIES[_h] for s in [e["surface"], *e["variants"]]]
    RE_TARGET[_h] = _alt_regex(_surfs, ignorecase=IGNORECASE_H[_h])

# compiled per-entity competing-sense excludes
EXCL_COMPILED = {h: {} for h in HIERARCHIES}
for _h in HIERARCHIES:
    for _e in ENTITIES[_h]:
        EXCL_COMPILED[_h][_e["surface"]] = [re.compile(p) for p in _e["excl"]]

# lowercase competitor words -> canonical surface (homograph_distractor source 2)
LC_COMPETITOR = {h: {} for h in HIERARCHIES}
for _h in HIERARCHIES:
    for _e in ENTITIES[_h]:
        for _w in _e["lc_comp"]:
            LC_COMPETITOR[_h][_w] = _e["surface"]
RE_LC_COMP = {}
for _h in HIERARCHIES:
    _ws = list(LC_COMPETITOR[_h].keys())
    RE_LC_COMP[_h] = (re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(w) for w in
                      sorted(_ws, key=len, reverse=True)) + r")(?![A-Za-z])") if _ws else None)


# ----------------------------------------------------------------------------- identity-sense local cues
# generic identity head nouns that follow the token (the dominant, high-precision accept path)
_NAT_HEAD = (r"(?:citizens?|nationals?|peoples?|people|immigrants?|migrants?|emigrants?|descent|origin|"
             r"ancestry|heritage|nationality|government|governments?|state|states|army|armies|navy|"
             r"forces|troops|soldiers?|officials?|diplomats?|ambassadors?|players?|team|teams|"
             r"athletes?|community|communities|population|populations?|families|family|man|men|woman|"
             r"women|workers?|students?|authors?|writers?|artists?|musicians?|leaders?|presidents?|"
             r"ministers?|companies|company|firms?|cuisine|food|dishes?|dish|languages?|language|"
             r"cultures?|culture|economy|economies|markets?|market|borders?|border|wars?|war|"
             r"revolution|history|politics|society|nationalism|diaspora|embassy|consulate|passports?|"
             r"citizenship|accent|dialect|empire|colon(?:y|ies)|territory|coast|flag|champion|"
             r"champions|delegation|refugees?|expats?|descendants?|voters?|electorate|votes?|"
             r"parliament|coalition|premier|presidency|senate|capital|currency|nationals?)")
_REL_HEAD = (r"(?:communit(?:y|ies)|faiths?|believers?|world|countr(?:y|ies)|families|family|man|men|"
             r"woman|women|clerics?|scholars?|leaders?|population|minorit(?:y|ies)|majorit(?:y|ies)|"
             r"prayers?|congregations?|schools?|church|churches|mosques?|temples?|synagogues?|"
             r"denominations?|traditions?|values|doctrines?|theology|practices?|holidays?|holiday|"
             r"festivals?|rituals?|teachings?|converts?|pilgrims?|missionar(?:y|ies)|Brotherhood|"
             r"charit(?:y|ies)|groups?|organi[sz]ations?|extremists?|fundamentalists?|clergy|priests?|"
             r"imams?|rabbis?|monks?|nuns?|cemetery|name|music|rock|band|bookstore|fellowship|sect|"
             r"sects|theologians?)")
_ETH_HEAD = (r"(?:peoples?|people|persons?|person|communit(?:y|ies)|Americans?|men|man|women|woman|"
             r"voters?|families|family|workers?|students?|population|residents?|neighbou?rhoods?|"
             r"churches?|church|cultures?|culture|history|leaders?|youth|children|kids|households?|"
             r"majorit(?:y|ies)|minorit(?:y|ies)|business(?:es)?|press|colleges?|Caucus|girls?|boys?|"
             r"folks|enrollment|descent|heritage|nationalis[mt]s?|supremac(?:y|ist|ists)|privilege|"
             r"immigrants?|owned|teens?|adults?|mothers?|fathers?|patients?|defendants?|officers?|"
             r"cops?|activists?|scholars?|writers?|artists?|athletes?|elders?|tribes?|nations?|"
             r"reservations?|rights|girl|boy|teenagers?|lawmakers?|candidates?|migrants?|slaves?|"
             r"diaspora|enslaved|farmers?|soldiers?|veterans?)")
INCL_RIGHT = {
    "nationality": re.compile(r"^[\s-]+" + _NAT_HEAD + r"\b", re.IGNORECASE),
    "religion": re.compile(r"^[\s-]+" + _REL_HEAD + r"\b", re.IGNORECASE),
    "ethnicity_identity": re.compile(r"^[\s-]+" + _ETH_HEAD + r"\b", re.IGNORECASE),
}
# plural-noun usage ("many Muslims believe", "Americans are")
PLURAL = {h: set() for h in HIERARCHIES}
for _h in ("nationality", "religion", "ethnicity_identity"):
    for _e in ENTITIES[_h]:
        for _s in _e["variants"]:
            if _s.endswith("s"):
                PLURAL[_h].add(_s)
        # also accept canonical noun-plurals that ARE the surface (e.g. Hispanic? no) handled via variants
LEFT_QUANT = re.compile(r"(?:\b(?:the|some|many|most|few|several|all|both|two|three|four|five|six|seven|"
                        r"eight|nine|ten|other|fellow|young|elderly|native|ethnic|of|millions|thousands|"
                        r"hundreds|dozens|number|group)\s+(?:of\s+)?)$", re.IGNORECASE)
RIGHT_VERBISH = re.compile(r"^[\s]*(?:[.,;:!?)]|(?:\s+(?:are|were|have|had|will|can|could|would|should|do|"
                           r"did|believe|think|thought|say|said|want|live|lived|face|faced|make|made|tend|"
                           r"often|also|who|that|in|across|around|and|of|from|with|like|as|were|remain|"
                           r"continue|account|represent|comprise|vote|voted|march|marched|protest|"
                           r"protested|gathered|gather)\b))")
PRED_LEFT = re.compile(r"(?:\b(?:is|are|was|were|be|been|being|am|a|an|as|half|part|ethnically|racially|"
                       r"culturally|both|becoming|became|become|considered|identif(?:y|ies|ied)\s+as|"
                       r"proudly|partly)\s+)$", re.IGNORECASE)
PRED_RIGHT = re.compile(r"^(?:[.,;:!?)\"']|-(?:American|Americans|born)|\s+(?:and|or|who|by|man|woman|men|"
                        r"women|guy|girl|kid|community|family|descent|heritage|origin|background|"
                        r"American|Americans|Muslim|citizen|national)\b|\s*$)")


def _ctx(win, s, e, nleft=24, nright=46):
    return win[max(0, s - nleft):s], win[e:e + nright]


def _excluded(h, surface_canon, win, s, e):
    """True iff this occurrence is in the entity's COMPETING (non-identity) sense."""
    pats = EXCL_COMPILED[h].get(surface_canon)
    if not pats:
        return False
    local = win[max(0, s - 22):e + 46]
    return any(p.search(local) for p in pats)


def _identity_ok(h, win, s, e, surface_text, surface_canon):
    """High-precision: is this occurrence the IDENTITY/target sense of the parent concept?"""
    if _excluded(h, surface_canon, win, s, e):
        return False
    left, right = _ctx(win, s, e)
    if INCL_RIGHT[h].match(right):                       # token + identity head noun (dominant path)
        return True
    if surface_text in PLURAL[h] and (LEFT_QUANT.search(left) or RIGHT_VERBISH.match(right)):
        return True                                      # plural people-noun usage
    if PRED_LEFT.search(left) and PRED_RIGHT.match(right):
        return True                                      # predicative "She is Polish."
    return False


# ----- named_entity_safety: person OR organisation cues (reuses iter-5 person/brand machinery) --------
_NE_PERSON_LEFT_TITLE = re.compile(r"(?:\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sir|Lady|President|Senator|Governor|"
                                   r"Mayor|Congressman|Congresswoman|Representative|Justice|Judge|Captain|"
                                   r"Coach|CEO|Chairman|Reverend|Rev|Saint|St|General|Director)\.?\s+)$")
_NE_PERSON_RIGHT_VERB = re.compile(r"^\s+(?:said|says|asked|replied|wrote|added|argued|announced|claimed|"
                                   r"insisted|admitted|denied|testified|won|lost|died|was\s+born|scored|"
                                   r"signed|told|stated|noted|explained|warned|urged|called|spoke|"
                                   r"resigned|stepped\s+down|endorsed|defeated|led)\b")
_NE_PERSON_RIGHT_POSS = re.compile(r"^'s\s+(?:campaign|presidency|administration|book|books|film|films|"
                                   r"movie|movies|album|albums|song|songs|team|company|career|speech|"
                                   r"victory|win|defeat|lawyer|spokesman|spokeswoman|office|tweet|"
                                   r"statement|comments?|remarks?|policy|policies|wife|husband|family)\b")
_NE_ORG_RIGHT = re.compile(r"^\s*(?:Inc\b|Corp\b|Co\b|Ltd\b|LLC\b|Plc\b|announced|released|launched|"
                           r"unveiled|reported|shares?\b|stock\b|stocks\b|CEO\b|earnings|revenue|"
                           r"profits?\b|products?\b|store\b|stores\b|app\b|apps\b|brand\b|company\b|"
                           r"customers\b|investors\b|acquired|acquires|sued|hired|fired|laid\s+off)")
_NE_ORG_POSS = re.compile(r"^'s\s+(?:new|latest|CEO|stock|shares|products?|earnings|revenue|app|store|"
                          r"brand|market|cloud|services?|platform|customers|business)\b")
_NE_ORG_LEFT = re.compile(r"(?:\b(?:shares?|stock|stocks|investors|analysts|shareholders)\s+(?:of|in|"
                          r"upgraded|downgraded|rated)\s+)$")


def named_entity_ok(win, s, e, surface_text=None, surface_canon=None):
    if _excluded("named_entity_safety", surface_canon, win, s, e):
        return False
    left, right = _ctx(win, s, e, nleft=22, nright=40)
    if _NE_PERSON_LEFT_TITLE.search(left):
        return True
    if _NE_PERSON_RIGHT_VERB.match(right) or _NE_PERSON_RIGHT_POSS.match(right):
        return True
    if _NE_ORG_RIGHT.match(right) or _NE_ORG_POSS.match(right):
        return True
    if _NE_ORG_LEFT.search(left):
        return True
    return False


def target_ok(h, win, s, e, surface_text, surface_canon):
    if h == "named_entity_safety":
        return named_entity_ok(win, s, e, surface_text, surface_canon)
    return _identity_ok(h, win, s, e, surface_text, surface_canon)


# ----------------------------------------------------------------------------- detectors
def detect_targets(win):
    """Return [(hierarchy, canonical_surface, matched_text, start, end)] for IDENTITY-sense matches."""
    out = []
    for h in HIERARCHIES:
        for m in RE_TARGET[h].finditer(win):
            s, e = m.start(1), m.end(1)
            txt = m.group(1)
            canon = SURFACE_TO_CANON[h].get(txt)
            if canon is None:
                # case-insensitive hierarchies: map by canonical-case lookup
                for cand, c in SURFACE_TO_CANON[h].items():
                    if cand.lower() == txt.lower():
                        canon = c
                        break
            if canon is None:
                continue
            if target_ok(h, win, s, e, txt, canon):
                out.append((h, canon, txt, s, e))
    return out


def detect_competitors(win):
    """Return [(hierarchy, canonical_surface, matched_text, start, end)] for COMPETING-sense matches
    (the homograph_distractor matched-negative family)."""
    out = []
    for h in HIERARCHIES:
        # source 1: a target surface in its excluded competing sense (e.g. 'Black Sea', 'Indian Ocean')
        for m in RE_TARGET[h].finditer(win):
            s, e = m.start(1), m.end(1)
            txt = m.group(1)
            canon = SURFACE_TO_CANON[h].get(txt) or next(
                (c for cand, c in SURFACE_TO_CANON[h].items() if cand.lower() == txt.lower()), None)
            if canon is None:
                continue
            if HOMOGRAPH.get((h, canon)) and _excluded(h, canon, win, s, e):
                out.append((h, canon, txt, s, e))
        # source 2: a dedicated lowercase competitor word (e.g. 'polish' the verb, 'apple' the fruit)
        rc = RE_LC_COMP[h]
        if rc is not None:
            for m in rc.finditer(win):
                out.append((h, LC_COMPETITOR[h][m.group(1)], m.group(1), m.start(1), m.end(1)))
    return out


def any_token(win):
    """True iff the window contains ANY target surface OR competitor token of any hierarchy."""
    for h in HIERARCHIES:
        if RE_TARGET[h].search(win):
            return True
        if RE_LC_COMP[h] is not None and RE_LC_COMP[h].search(win):
            return True
    return False


# ----------------------------------------------------------------------------- templated pair frames
# Content-flip frames: x_on = identity token (target sense, positive); x_off = a surface-matched
# NON-identity filler from OFF_POOLS (parent absent, negative). Templates force the identity sense.
CONTENT_FRAMES = {
    "nationality": [
        ("nx1", "The {S} government announced sweeping new reforms.", "non_identity"),
        ("nx2", "The {S} economy expanded rapidly last year.", "non_identity"),
        ("nx3", "The {S} community celebrated the holiday together.", "non_identity"),
        ("nx4", "A group of {S} workers went on strike.", "non_identity"),
        ("nx5", "The {S} team won the championship.", "non_identity"),
        ("nx6", "The {S} delegation arrived for the summit.", "non_identity"),
        ("nx7", "Many {S} families settled in the region.", "non_identity"),
        ("nx8", "The {S} army withdrew from the border.", "non_identity"),
    ],
    "religion": [
        ("rx1", "The {S} community gathered for the festival.", "non_identity"),
        ("rx2", "Many {S} families attend services every week.", "non_identity"),
        ("rx3", "The {S} leaders issued a joint statement.", "non_identity"),
        ("rx4", "A {S} charity distributed food to the poor.", "non_identity"),
        ("rx5", "The {S} school added new classes this year.", "non_identity"),
        ("rx6", "Several {S} groups organized the event.", "non_identity"),
    ],
    "ethnicity_identity": [
        ("ex1", "The {S} community organized a rally downtown.", "non_identity"),
        ("ex2", "Many {S} voters supported the measure.", "non_identity"),
        ("ex3", "The {S} families lived in the same neighborhood.", "non_identity"),
        ("ex4", "A group of {S} students formed the club.", "non_identity"),
        ("ex5", "The {S} population grew over the decade.", "non_identity"),
        ("ex6", "The {S} workers demanded better pay.", "non_identity"),
    ],
    "named_entity_safety": [
        ("sx1", "{S} announced the decision on Monday.", "non_identity"),
        ("sx2", "{S} declined to comment on the report.", "non_identity"),
        ("sx3", "{S} faced criticism over the new policy.", "non_identity"),
        ("sx4", "{S} attracted attention from the media.", "non_identity"),
        ("sx5", "{S} received an award last week.", "non_identity"),
        ("sx6", "{S} appeared in the headlines again.", "non_identity"),
    ],
}

# A second, sharper hard-negative: x_off = a DIFFERENT identity-category word that is NOT a member of
# this hierarchy's parent (tests parent specificity). Filled per hierarchy in OFF_POOLS['other_group'].
CONTENT_FRAMES_OTHER = {
    "nationality": ("no1", "The {S} community celebrated the holiday together."),
    "religion": ("ro1", "The {S} community gathered for the festival."),
    "ethnicity_identity": ("eo1", "The {S} community organized a rally downtown."),
}

OFF_POOLS = {
    # non-identity fillers (grammatical pre-nominal adjectives / generic subjects) for each hierarchy
    "nationality": ["local", "regional", "central", "modern", "rural", "urban", "young", "large",
                    "private", "coastal", "northern", "southern", "working"],
    "religion": ["local", "online", "rural", "student", "village", "regional", "volunteer",
                 "farming", "fishing", "coastal", "neighboring", "young"],
    "ethnicity_identity": ["local", "rural", "urban", "young", "suburban", "farming", "working",
                           "college", "regional", "coastal", "downtown", "veteran"],
    "named_entity_safety": ["The mayor", "The agency", "The committee", "The startup", "The senator",
                            "The author", "The bank", "The professor", "The retailer", "The official",
                            "The regulator", "The council"],
    # other-group hard negatives: identity words from OTHER hierarchies (not this parent's members)
    "other_group_for_nationality": ["Muslim", "Christian", "Buddhist", "Hindu", "Catholic", "Sikh",
                                    "Jewish", "Hispanic", "Protestant", "Mormon", "Latino", "Atheist"],
    "other_group_for_religion": ["American", "Russian", "Mexican", "Black", "Latino", "Asian",
                                 "Chinese", "German", "Hispanic", "Arab", "Canadian", "French"],
    "other_group_for_ethnicity_identity": ["Muslim", "Christian", "Buddhist", "Canadian", "French",
                                           "Hindu", "Sikh", "American", "Russian", "Catholic", "German",
                                           "Mormon"],
}

# Surface-flip frames: BOTH carriers positive (identity sense fixed), for the surface-invariance check.
SURFACE_FRAMES = {
    "nationality": ["The {S} delegation met with trade officials.",
                    "She is proud of her {S} heritage.",
                    "Reporters interviewed several {S} citizens.",
                    "The {S} economy depends heavily on exports.",
                    "He grew up in a close-knit {S} community.",
                    "The {S} government denied the allegations."],
    "religion": ["The {S} community holds services every Friday.",
                 "She was raised in a devout {S} family.",
                 "The {S} leaders called for calm.",
                 "Members of the {S} faith gathered to pray.",
                 "The {S} charity runs several shelters.",
                 "He studied the history of the {S} tradition."],
    "ethnicity_identity": ["The {S} community has grown in recent years.",
                           "She writes about {S} history and culture.",
                           "Many {S} families moved to the suburbs.",
                           "The {S} students started a mentorship program.",
                           "Polls show {S} voters are divided.",
                           "The report highlights disparities for {S} workers."],
    "named_entity_safety": ["{S} reported strong results this quarter.",
                            "Critics praised the latest move by {S}.",
                            "{S} has been in the news all week.",
                            "Investors remain optimistic about {S}.",
                            "{S} issued a public apology on Tuesday.",
                            "Many people closely follow {S}."],
}


# ----------------------------------------------------------------------------- row builder
def find_slot(template: str) -> int:
    return template.index("{S}")


def make_row(*, input_text, output, hierarchy, row_type, sub_context, pair_id, pair_role,
             target_text, target_char_start, target_char_end, source, pile_set_name=None,
             llm_judge_pass=None, llm_judge_score=None, fold=None, template_id=None,
             neg_family=None, entity=None, target_sense=None, homograph_sense=None,
             dominant_other_sense=None, homograph_strength_val=None, multi_token=None,
             identity_label_source=None, notes=None):
    return {
        "input": input_text,
        "output": output,
        "metadata_hierarchy": hierarchy,
        "metadata_row_type": row_type,
        "metadata_concept_present": (output == "positive"),
        "metadata_sub_context": sub_context,
        "metadata_parent_concept": PARENT_CONCEPT[hierarchy],
        "metadata_pair_id": pair_id,
        "metadata_pair_role": pair_role,
        "metadata_target_text": target_text,
        "metadata_target_char_start": target_char_start,
        "metadata_target_char_end": target_char_end,
        "metadata_target_token_indices": None,   # filled in tokenization pass
        "metadata_multi_token": multi_token,     # filled/normalized in tokenization pass
        "metadata_source": source,
        "metadata_pile_set_name": pile_set_name,
        "metadata_llm_judge_pass": llm_judge_pass,
        "metadata_llm_judge_score": llm_judge_score,
        "metadata_fold": fold,
        "metadata_template_id": template_id,
        "metadata_neg_family": neg_family,
        "metadata_entity": entity,
        "metadata_target_sense": target_sense,
        "metadata_homograph_sense": homograph_sense,
        "metadata_dominant_other_sense": dominant_other_sense,
        "metadata_homograph_strength": homograph_strength_val,
        "metadata_safety_relevant": SAFETY_RELEVANT,
        "metadata_identity_label_source": identity_label_source,
        "metadata_notes": notes,
    }


def _ent_fields(hierarchy, canon):
    e = ENT_BY_CANON[hierarchy].get(canon, {})
    return dict(homograph_sense=bool(e.get("homograph")),
                dominant_other_sense=e.get("gloss"),
                homograph_strength_val=e.get("strength"),
                multi_token=(" " in canon or "-" in canon))


def build_content_pair(*, hierarchy, entity, template, off_filler, pair_id, source, template_id,
                       neg_family, notes=None):
    """(x_on, x_off) content-flip pair; one template, surface constant within the pair."""
    slot = find_slot(template)
    x_on = template.replace("{S}", entity)
    x_off = template.replace("{S}", off_filler)
    on_start, on_end = slot, slot + len(entity)
    ef = _ent_fields(hierarchy, entity)
    coll = COLLISIONS.get(entity)
    note_on = "; ".join([x for x in (notes, (f"collision: {coll}" if coll else None)) if x]) or None
    row_on = make_row(input_text=x_on, output="positive", hierarchy=hierarchy, row_type="content_pair",
                      sub_context=entity, pair_id=pair_id, pair_role="x_on", target_text=entity,
                      target_char_start=on_start, target_char_end=on_end, source=source,
                      template_id=template_id, neg_family=neg_family, entity=entity,
                      target_sense=hierarchy, notes=note_on, **ef)
    # x_off slot is zero-width at the differing position (concept absent)
    row_off = make_row(input_text=x_off, output="negative", hierarchy=hierarchy, row_type="content_pair",
                       sub_context=None, pair_id=pair_id, pair_role="x_off", target_text="",
                       target_char_start=slot, target_char_end=slot, source=source,
                       template_id=template_id, neg_family=neg_family, entity=None, target_sense=None,
                       homograph_sense=None, dominant_other_sense=None, homograph_strength_val=None,
                       multi_token=False, notes=f"off_filler={off_filler!r}")
    return [row_on, row_off]


def build_surface_pair(*, hierarchy, entity, frame_a, frame_b, pair_id, source, notes=None):
    """(surface_a, surface_b): same identity token (target sense), two different carriers (both positive)."""
    rows = []
    ef = _ent_fields(hierarchy, entity)
    coll = COLLISIONS.get(entity)
    note = "; ".join([x for x in (notes, (f"collision: {coll}" if coll else None)) if x]) or None
    for role, frame in (("surface_a", frame_a), ("surface_b", frame_b)):
        slot = find_slot(frame)
        text = frame.replace("{S}", entity)
        rows.append(make_row(input_text=text, output="positive", hierarchy=hierarchy,
                             row_type="surface_pair", sub_context=entity, pair_id=pair_id,
                             pair_role=role, target_text=entity, target_char_start=slot,
                             target_char_end=slot + len(entity), source=source, neg_family=None,
                             entity=entity, target_sense=hierarchy, notes=note, **ef))
    return rows


if __name__ == "__main__":
    logger.info(f"hierarchies={HIERARCHIES}  wordfreq_ok={WORDFREQ_OK}")
    for h in HIERARCHIES:
        homs = [e["surface"] for e in ENTITIES[h] if e["homograph"]]
        logger.info(f"{h}: {len(ENTITIES[h])} entities; homographs={homs}")
    demo = ("Polish voters and the Polish government met Muslim community leaders. Black families and "
            "white voters disagreed. He likes to polish his shoes near the Black Sea. Apple announced "
            "earnings while Bush declined to comment. Christian Bale starred in the film. The Indian "
            "Ocean is warm but Indian citizens protested. She bought a black car and white wine.")
    logger.info(f"targets: {detect_targets(demo)}")
    logger.info(f"competitors: {detect_competitors(demo)}")
