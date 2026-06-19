#!/usr/bin/env python3
"""Assemble references.bib: match fetched S2 entries to canonical paper-text keys,
rewrite citation keys, and append hand-written entries for items S2 lacks."""
import json
import re

refs = json.load(open("refs_all.json"))
res = json.load(open("bib_result2.json"))
entries = res.get("entries", [])


def norm_arxiv(a):
    if not a:
        return ""
    a = str(a).lower().strip()
    a = re.sub(r"v\d+$", "", a)
    return a


def norm_doi(d):
    return str(d).lower().strip() if d else ""


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", str(t).lower()) if t else ""


# index entries
by_arxiv = {norm_arxiv(e.get("arxiv")): e for e in entries if e.get("arxiv")}
by_doi = {norm_doi(e.get("doi")): e for e in entries if e.get("doi")}
by_title = {norm_title(e.get("title")): e for e in entries if e.get("title")}

out = []
matched_keys = set()
unmatched = []

for r in refs:
    key = r["key"]
    e = None
    if r.get("arxiv") and norm_arxiv(r["arxiv"]) in by_arxiv:
        e = by_arxiv[norm_arxiv(r["arxiv"])]
    elif r.get("doi") and norm_doi(r["doi"]) in by_doi:
        e = by_doi[norm_doi(r["doi"])]
    elif r.get("title"):
        nt = norm_title(r["title"])
        if nt in by_title:
            e = by_title[nt]
        else:
            # fuzzy: title prefix overlap
            for et, ev in by_title.items():
                if nt[:40] and (nt[:40] in et or et[:40] in nt):
                    e = ev
                    break
    if e is None:
        unmatched.append(key)
        continue
    bib = e["bibtex"].strip()
    # rewrite the citation key on the first line: @type{OLDKEY,
    bib = re.sub(r"^(@\w+\{)[^,]+,", r"\1" + key + ",", bib, count=1)
    out.append(bib)
    matched_keys.add(key)

# Hand-written entries (verified metadata; not indexed cleanly by S2)
handwritten = {
    "Templeton2024": r"""@misc{Templeton2024,
  title = {Scaling Monosemanticity: Extracting Interpretable Features from {Claude} 3 {Sonnet}},
  author = {Templeton, Adly and Conerly, Tom and Marcus, Jonathan and Lindsey, Jack and Bricken, Trenton and Chen, Brian and Pearce, Adam and Citro, Craig and Ameisen, Emmanuel and Jones, Andy and Cunningham, Hoagy and Turner, Nicholas L. and McDougall, Callum and MacDiarmid, Monte and Tamkin, Alex and Durmus, Esin and Hume, Tristan and Mosconi, Francesco and Freeman, C. Daniel and Sumers, Theodore R. and Rees, Edward and Batson, Joshua and Jermyn, Adam and Carter, Shan and Olah, Chris and Henighan, Tom},
  year = {2024},
  howpublished = {Transformer Circuits Thread},
  url = {https://transformer-circuits.pub/2024/scaling-monosemanticity/}
}""",
    "Bricken2023": r"""@misc{Bricken2023,
  title = {Towards Monosemanticity: Decomposing Language Models With Dictionary Learning},
  author = {Bricken, Trenton and Templeton, Adly and Batson, Joshua and Chen, Brian and Jermyn, Adam and Conerly, Tom and Turner, Nick and Anil, Cem and Denison, Carson and Askell, Amanda and Lasenby, Robert and Wu, Yifan and Kravec, Shauna and Schiefer, Nicholas and Maxwell, Tim and Joseph, Nicholas and Hatfield-Dodds, Zac and Tamkin, Alex and Nguyen, Karina and McLean, Brayden and Burke, Josiah E. and Hume, Tristan and Carter, Shan and Henighan, Tom and Olah, Christopher},
  year = {2023},
  howpublished = {Transformer Circuits Thread},
  url = {https://transformer-circuits.pub/2023/monosemantic-features/}
}""",
    "Rudner2024": r"""@inproceedings{Rudner2024,
  title = {Mind the {GAP}: Improving Robustness to Subpopulation Shifts with Group-Aware Priors},
  author = {Rudner, Tim G. J. and Zhang, Ya Shi and Wilson, Andrew Gordon and Kempe, Julia},
  booktitle = {Proceedings of the 27th International Conference on Artificial Intelligence and Statistics (AISTATS)},
  year = {2024}
}""",
    "Feige1998": r"""@article{Feige1998,
  title = {A threshold of $\ln n$ for approximating set cover},
  author = {Feige, Uriel},
  journal = {Journal of the ACM},
  volume = {45},
  number = {4},
  pages = {634--652},
  year = {1998},
  doi = {10.1145/285055.285059}
}""",
}

for key, bib in handwritten.items():
    if key not in matched_keys:
        out.append(bib)
        matched_keys.add(key)

with open("references.bib", "w") as f:
    f.write("\n\n".join(out) + "\n")

print("Wrote", len(out), "entries to references.bib")
still_missing = [k for k in unmatched if k not in matched_keys]
print("Still missing (need attention):", still_missing)
print("Total canonical keys covered:", len(matched_keys))
