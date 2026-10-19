#!/usr/bin/env python3
"""Generate included.bib from extraction_matrix.csv (keys ref<id>)."""
import csv
import os

ROOT = "/mnt/drive2/newpaper"
rows = list(csv.DictReader(open(os.path.join(ROOT, "analysis", "extraction_matrix.csv"), encoding="utf-8")))

SPECIAL = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}


def esc(s):
    for k, v in SPECIAL.items():
        s = s.replace(k, v)
    return s


def author(r):
    ORG = ("labs", "university", "inc", "corp", "institute", "technologist", "college")
    parts = []
    for a in r["authors"].split(";"):
        a = " ".join(a.split()).replace(",", " ")
        if not a or len(a.split()) > 5 or any(w in a.lower() for w in ORG):
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
       "}", ""]

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
        venue = "  howpublished = {" + esc(r["venue"]) + " (" + r["venue_type"] + ")}, "
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
