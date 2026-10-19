#!/usr/bin/env python3
"""Generate included.bib from extraction_matrix.csv (keys ref<id>)."""
import csv
import os
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(ROOT, "analysis", "extraction_matrix.csv"), encoding="utf-8")))

SPECIAL = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}

# Characters that T1 (EC fonts) cannot render, mapped to safe equivalents.
DASHES = {"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "--",
          "\u2014": "---", "\u2015": "--", "\u2212": "-"}
QUOTES = {"\u2018": "'", "\u2019": "'", "\u201a": ",", "\u201c": '"',
          "\u201d": '"', "\u201e": '"', "\u0131": "i", "\u0130": "I",
          "\u00a0": " "}

# Cyrillic -> Latin (passport-style), so Russian/Kazakh names never hit the
# latin-1 fallback that used to render them as '?' in the compiled PDF.
CYR = {"\u0430": "a", "\u0431": "b", "\u0432": "v", "\u0433": "g",
       "\u0434": "d", "\u0435": "e", "\u0451": "e", "\u0436": "zh", "\u0437": "z",
       "\u0438": "i", "\u0439": "y", "\u043a": "k", "\u043b": "l", "\u043c": "m",
       "\u043d": "n", "\u043e": "o", "\u043f": "p", "\u0440": "r", "\u0441": "s",
       "\u0442": "t", "\u0443": "u", "\u0444": "f", "\u0445": "kh", "\u0446": "ts",
       "\u0447": "ch", "\u0448": "sh", "\u0449": "shch", "\u044a": "", "\u044b": "y",
       "\u044c": "", "\u044d": "e", "\u044e": "yu", "\u044f": "ya"}
for _lo, _hi in list(CYR.items()):
    CYR[_lo.upper()] = _hi.capitalize()


def normalize(s):
    """Transliterate to LaTeX-safe, T1-renderable text."""
    for src, dst in DASHES.items():
        s = s.replace(src, dst)
    for src, dst in QUOTES.items():
        s = s.replace(src, dst)
    for src, dst in CYR.items():
        s = s.replace(src, dst)
    # NFKD + strip combining marks handles ă, ş, İ, č, etc.
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    # any remaining non-Latin-1 char: drop to ASCII via latin-1 round trip
    s = s.encode("latin-1", "replace").decode("latin-1")
    return s.replace("\ufffd", "")


def esc(s):
    s = normalize(s)
    for k, v in SPECIAL.items():
        s = s.replace(k, v)
    return s


def author(r):
    # substring filter for org names that spell out, plus an exact-token filter
    # for short org tokens that must not hit person names (e.g. 'REC', 'QHSE')
    ORG_SUB = ("labs", "university", "inc", "corp", "institute", "technologist",
               "college", "ministry", "department of", "national laboratory")
    ORG_TOK = {"rec", "qhse", "ltd", "llc", "gmbh", "plc", "jsc", "usdoe", "doe"}
    parts = []
    raw = r["authors"]
    # semicolon-separated is the norm; fall back to commas when no ';' present
    segments = raw.split(";") if ";" in raw else raw.split(",")
    for a in segments:
        a = normalize(" ".join(a.split()).replace(",", " "))
        if not a or len(a.split()) > 5 or any(w in a.lower() for w in ORG_SUB):
            continue
        if any(tok in ORG_TOK for tok in a.lower().split()):
            continue
        parts.append(a)
    return " and ".join(parts) if parts else "{\\textit{Authors unreported in source}}"


out = ["% Auto-generated from analysis/extraction_matrix.csv - do not hand-edit.",
       "% Vernacular entry for the competitor (three authors, outer list not expanded):",
       "@article{habeeb2026,",
       "  author  = {Habeeb, W. and Weli, A. and Almaliki, A.},",
       "  title   = {From attack surface to security asset: a systematic review of Dual-Role Digital Twins in cyber-physical security (2019--2025)},",
       "  journal = {Digital Twin},",
       "  year    = {2026},",
       "  doi     = {10.1080/27525783.2026.2679856}",
       "}",
       "",
       "% Foundational (non-corpus) background references. All DOIs verified against",
       "% Crossref on 2026-10-19 (scripts/verify_background_refs.py in the worklog trail);",
       "% entries without DOIs are reports/preprints cited as such.",
       "@article{liu2011,",
       "  author  = {Liu, Y. and Ning, P. and Reiter, M. K.},",
       "  title   = {False data injection attacks against state estimation in electric power grids},",
       "  journal = {ACM Transactions on Information and System Security},",
       "  volume  = {14},",
       "  number  = {1},",
       "  pages   = {1--33},",
       "  year    = {2011},",
       "  doi     = {10.1145/1952982.1952995}",
       "}",
       "@article{liang2017,",
       "  author  = {Liang, G. and Zhao, J. and Luo, F. and Weller, S. R. and Dong, Z. Y.},",
       "  title   = {A review of false data injection attacks against modern power systems},",
       "  journal = {IEEE Transactions on Smart Grid},",
       "  volume  = {8},",
       "  number  = {4},",
       "  pages   = {1630--1638},",
       "  year    = {2017},",
       "  doi     = {10.1109/TSG.2015.2495133}",
       "}",
       "@inproceedings{glaessgen2012,",
       "  author    = {Glaessgen, E. and Stargel, D.},",
       "  title     = {The digital twin paradigm for future {NASA} and {U.S. Air Force} vehicles},",
       "  booktitle = {53rd AIAA/ASME/ASCE/AHS/ASC Structures, Structural Dynamics and Materials Conference},",
       "  year      = {2012},",
       "  doi       = {10.2514/6.2012-1818}",
       "}",
       "@misc{grieves2014,",
       "  author       = {Grieves, M.},",
       "  title        = {Digital twin: manufacturing excellence through virtual factory replication},",
       "  howpublished = {White paper, Florida Institute of Technology},",
       "  year         = {2014}",
       "}",
       "@article{tao2019,",
       "  author  = {Tao, F. and Zhang, H. and Liu, A. and Nee, A. Y. C.},",
       "  title   = {Digital twin in industry: State-of-the-art},",
       "  journal = {IEEE Transactions on Industrial Informatics},",
       "  volume  = {15},",
       "  number  = {4},",
       "  pages   = {2405--2415},",
       "  year    = {2019},",
       "  doi     = {10.1109/TII.2018.2873186}",
       "}",
       "@misc{szegedy2014,",
       "  author       = {Szegedy, C. and Zaremba, W. and Sutskever, I. and Bruna, J. and Erhan, D. and Goodfellow, I. and Fergus, R.},",
       "  title        = {Intriguing properties of neural networks},",
       "  howpublished = {arXiv preprint arXiv:1312.6199; ICLR 2014},",
       "  year         = {2014}",
       "}",
       "@misc{goodfellow2015,",
       "  author       = {Goodfellow, I. J. and Shlens, J. and Szegedy, C.},",
       "  title        = {Explaining and harnessing adversarial examples},",
       "  howpublished = {arXiv preprint arXiv:1412.6572; ICLR 2015},",
       "  year         = {2015}",
       "}",
       "@article{biggio2018,",
       "  author  = {Biggio, B. and Roli, F.},",
       "  title   = {Wild patterns: Ten years after the rise of adversarial machine learning},",
       "  journal = {Pattern Recognition},",
       "  volume  = {84},",
       "  pages   = {317--331},",
       "  year    = {2018},",
       "  doi     = {10.1016/j.patcog.2018.07.023}",
       "}",
       "@techreport{eisac2016,",
       "  author      = {{Electricity Information Sharing and Analysis Center (E-ISAC)}},",
       "  title       = {Analysis of the cyber attack on the {Ukrainian} power grid: Defense use case},",
       "  institution = {SANS Industrial Control Systems},",
       "  year        = {2016}",
       "}",
       ""]

for r in rows:
    key = f"ref{r['id']}"
    a = author(r)
    if r["venue_type"] == "journal":
        typ = "@article{"
        venue = "  journal = {" + esc(r["venue"]) + "},"
    elif r["venue_type"] == "conference":
        typ = "@inproceedings{"
        venue = "  booktitle = {" + esc(r["venue"]) + "},"
    else:
        typ = "@misc{"
        # venue_type contains underscores (book_chapter): use a printable label
        vtype = r["venue_type"].replace("_", " ")
        # avoid duplicating a type label the venue string already carries
        if f"({vtype})" in r["venue"].lower() or f"({vtype})" in r["venue"]:
            venue = "  howpublished = {" + esc(r["venue"]) + "}, "
        else:
            venue = "  howpublished = {" + esc(r["venue"]) + " (" + vtype + ")}, "
    entry = [f"{typ}{key},",
             f"  author = {{{a}}},",
             f"  title = {{{esc(r['title'])}}},",
             venue,
             f"  year = {{{r['year']}}},"]
    if r["doi"].strip():
        entry.append(f"  doi = {{{r['doi']}}},")
    entry[-1] = entry[-1].rstrip(",")
    entry.append("}")
    out.append("\n".join(entry))
    out.append("")

open(os.path.join(ROOT, "included.bib"), "w", encoding="utf-8").write("\n".join(out))
print("wrote included.bib:", len(rows), "entries")
