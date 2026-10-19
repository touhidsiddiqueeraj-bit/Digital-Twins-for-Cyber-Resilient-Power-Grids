#!/usr/bin/env python3
"""Generate appendix_corpus.tex (Appendix A: the 100 included studies).

Emits a longtable with a per-record Cit. column — cited_by at retrieval, taken from
digital_twin_grid_cybersecurity_papers.csv and joined positionally with a DOI
cross-check — so the ID display order (year descending, citations descending within
each year block) is verifiable from the paper itself.

Self-checks (exit 1 on violation): matrix order == ID order; IDs 1-45 all 2026 and
no 2026 beyond ID 45; citations non-increasing within every year block; exactly 40
zero-citation records. These are the claims §4.3 and the Appendix A caption make.
"""
import csv
import os
import sys
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(ROOT, "analysis", "extraction_matrix.csv")
PAPERS = os.path.join(ROOT, "digital_twin_grid_cybersecurity_papers.csv")
OUT = os.path.join(ROOT, "appendix_corpus.tex")

DASHES = {"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "--",
          "\u2014": "---", "\u2015": "--", "\u2212": "-"}


def normalize(s):
    for src, dst in DASHES.items():
        s = s.replace(src, dst)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.encode("latin-1", "replace").decode("latin-1")
    return s.replace("\ufffd", "")


def esc(s):
    s = normalize(s)
    return (s.replace("\\", "").replace("&", r"\&").replace("%", r"\%")
             .replace("_", r"\_").replace("#", r"\#").replace("~", " ").replace("^", ""))


def first_author(authors):
    a = normalize(authors.split(";")[0].strip())
    a = " ".join(a.split())
    if not a:
        return "Unattributed"
    return a if len(a) <= 38 else a[:35] + "..."


rows = list(csv.DictReader(open(MATRIX, encoding="utf-8")))
papers = list(csv.DictReader(open(PAPERS, encoding="utf-8")))
if len(rows) != len(papers) != 100:
    sys.exit(f"row-count mismatch: matrix {len(rows)} vs papers {len(papers)}")

# Positional join for cited_by; DOI cross-check where both sides have one.
mismatch = [r["id"] for r, p in zip(rows, papers)
            if r["doi"].strip() and p["doi"].strip()
            and r["doi"].strip().lower() != p["doi"].strip().lower()]
if mismatch:
    sys.exit(f"DOI positional mismatch at ids {mismatch}; refusing to write")

cits = []
for r, p in zip(rows, papers):
    try:
        cits.append(int(p["cited_by"] or 0))
    except ValueError:
        sys.exit(f"non-numeric cited_by for id {r['id']}: {p['cited_by']!r}")

# --- self-checks: the ordering claims made in §4.3 and the Appendix A caption ---
ids = [int(r["id"]) for r in rows]
years = [int(r["year"]) for r in rows]
if ids != list(range(1, 101)):
    sys.exit(f"matrix not in ID order: {ids[:5]}...")
if any(y != 2026 for y in years[:45]) or (len(years) > 45 and years[45] == 2026):
    sys.exit("year blocks do not match 'IDs 1-45 are all 2026'")
viol = []
prev_y, prev_c = None, None
for i, y, c in zip(ids, years, cits):
    if y != prev_y:
        prev_y, prev_c = y, None
    if prev_c is not None and c > prev_c:
        viol.append((i, y, c, prev_c))
    prev_c = c if prev_c is None else min(prev_c, c)
if viol:
    sys.exit(f"citations not descending within year blocks at: {viol}")
zeros = sum(1 for c in cits if c == 0)
if zeros != 40:
    sys.exit(f"zero-citation count is {zeros}, but §4.3 states 40")
print(f"self-checks passed: IDs 1-45 all 2026; citations descend within every "
      f"year block; {zeros}/100 zero-citation")

VT = {"journal": "journal", "conference": "conf.", "thesis": "thesis",
      "preprint": "preprint", "report": "report", "book_chapter": "chapter"}

L = []
L.append(r"\section*{Appendix A. The 100 included studies}\label{app:corpus}")
L.append("")
L.append(r"Table~\ref{tab:corpus} lists every record in the retained corpus, so that the")
L.append(r"included-study set is visible in the paper itself and not only in the released")
L.append(r"data. Citation scheme: IDs are corpus record numbers, cited in the running text as")
L.append(r"R$<$ID$>$; each record's full bibliographic entry appears in the reference list under")
L.append(r"the key \texttt{ref$<$ID$>$} (with DOI where one exists), so no separate mapping")
L.append(r"between the two schemes is needed. The IDs")
L.append(r"are a display order---year descending, and within each year block citations")
L.append(r"descending (IDs 1--45 are all 2026)---as the Cit.\ column shows. That ordering is")
L.append(r"a property of the export, not evidence about the selection rule that retained")
L.append(r"these 100 of the 492 eligible records; the comparison that would establish the")
L.append(r"rule is the year distribution of the 492 eligible records against the retained")
L.append(r"100, and the candidate-pool export it requires is listed as an unreleased")
L.append(r"artifact in the search-provenance manifest (Section~\ref{sec:method}).")
L.append(r"``FT'' marks the 83 records coded at full text; the 17 abstract-only records")
L.append(r"were coded at abstract level, with full-text fields treated as missing.")
L.append(r"R18, R59, R69 and R97 fall outside the strict grid scope of")
L.append(r"Section~\ref{sec:ai-threats}; R34, R68 and R84 are the borderline cases there.")
L.append(r"R69 carries unattributed authorship (Section~\ref{sec:validity}).")
L.append("")
L.append(r"\setlength{\tabcolsep}{4pt}")
L.append(r"\begin{longtable}{@{}r p{5.9cm} p{4.4cm} r r@{}}")
L.append(r"\caption{The retained corpus ($n=100$). IDs are a display order: year")
L.append(r"descending, citations descending within each year block (Cit.\ column).")
L.append(r"Citation counts are as retrieved at selection. DOIs are in the reference-list")
L.append(r"entries (keys \texttt{ref$<$ID$>$}).}\label{tab:corpus}\\")
L.append(r"\toprule")
L.append(r"ID & Study (first author) & Venue (type) & Cit. & FT \\")
L.append(r"\midrule")
L.append(r"\endfirsthead")
L.append(r"\multicolumn{5}{l}{\emph{Table~\ref{tab:corpus} continued}}\\")
L.append(r"\toprule")
L.append(r"ID & Study (first author) & Venue (type) & Cit. & FT \\")
L.append(r"\midrule")
L.append(r"\endhead")
L.append(r"\bottomrule")
L.append(r"\endfoot")
L.append(r"\endlastfoot")
for r, c in zip(rows, cits):
    venue = esc(r["venue"])
    if len(venue) > 52:
        venue = venue[:49] + "..."
    L.append(f"{r['id']} & {esc(first_author(r['authors']))} ({esc(r['year'])}) & "
             f"{venue} ({VT[r['venue_type']]}) & {c} & "
             f"{'Y' if r['fulltext']=='yes' else '--'} \\\\")
L.append(r"\end{longtable}")

open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"wrote {OUT} with {len(rows)} rows (Cit. column added)")
