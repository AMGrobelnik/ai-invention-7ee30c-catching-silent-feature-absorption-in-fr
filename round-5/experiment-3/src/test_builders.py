#!/usr/bin/env python
"""CPU-only validation of the M6c internal-spelling builders: vocab recipe, carrier rendering + char-span
consistency, and the Pile-window re-scan. NO GPU/model -- only the tokenizer + numpy."""
import numpy as np
from transformers import AutoTokenizer
import method as M

tok = AutoTokenizer.from_pretrained(M.MODEL_ID)
print("vocab_size", tok.vocab_size)

# 1) vocab recipe
by_letter, id_to_word = M._spelling_vocab(tok)
for L in M.NEW_LETTERS:
    ws = by_letter.get(L.lower(), [])
    print(f"  letter {L}: {len(ws)} slot-eligible vocab words; e.g.", [w['word'] for w in ws[:5]])
    assert len(ws) > 50, f"letter {L} too few vocab words"

# 2) carrier rendering + char-span consistency (the target token(s) recovered by _target_positions)
rng = np.random.default_rng(0)
ok = bad = 0
for tid in ["t_verbose", "t_colon", "t_icl"]:
    for w in ["Cat", "Banana", "Forest", "Mountain", "Planet", "River", "Window"]:
        text, span = M._render_carrier(tid, w, rng)
        enc = tok(text, return_offsets_mapping=True, add_special_tokens=True)
        offs = enc["offset_mapping"]; ids = enc["input_ids"]
        pos = M._target_positions(offs, span, None, len(ids))
        # the decoded selected tokens should reconstruct (start of) the target word
        sel = tok.decode([ids[p] for p in pos]).strip()
        good = sel.lower().startswith(w[:3].lower()) or w.lower().startswith(sel.lower()[:3])
        ok += good; bad += (not good)
        if not good:
            print(f"   MISMATCH carrier={tid} word={w!r} span={span} sel={sel!r} text={text[:40]!r}")
print(f"  carrier span check: {ok} ok / {bad} bad")
assert bad == 0

# 3) scan a small subset of Pile windows (CPU)
class _StubEnc:
    def __init__(self, tok): self.tok = tok
stub = _StubEnc(tok)
# monkeypatch DATA scan to use the real corpus but only scan via the function (it loads full data)
scan = M.scan_corpus_positives(stub, id_to_word, M.NEW_LETTERS, "mini")
for L in M.NEW_LETTERS:
    rows = scan[L]
    words = {}
    for r in rows:
        words[r["word"]] = words.get(r["word"], 0) + 1
    n_qual = sum(1 for c in words.values() if c >= M.MIN_SUB_TOKEN)
    print(f"  scan {L}: {len(rows)} occurrences, {len(words)} words, {n_qual} words >= MIN_SUB_TOKEN({M.MIN_SUB_TOKEN})")

# 4) verify a scanned positive's char span recovers the recorded token id on re-tokenization
nchk = 0
for L in M.NEW_LETTERS:
    for r in scan[L][:30]:
        enc = tok(r["input"], return_offsets_mapping=True, add_special_tokens=True)
        offs = enc["offset_mapping"]; ids = enc["input_ids"]
        pos = M._target_positions(offs, r["char_span"], None, len(ids))
        assert pos, f"no position for {r}"
        assert int(ids[pos[-1]]) == r["token_id"], f"token-id mismatch {L}: {int(ids[pos[-1]])} != {r['token_id']}"
        nchk += 1
print(f"  re-tokenization token-id self-check: {nchk} positives, 0 mismatches")
print("ALL BUILDER TESTS PASSED")
