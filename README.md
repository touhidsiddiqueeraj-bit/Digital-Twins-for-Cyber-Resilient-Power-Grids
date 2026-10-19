# Digital Twins for Cyber-Resilient Power Grids

**A Systematic Review and a Research Agenda for the AI-Powered Era**

Code, data, and manuscript for a PRISMA-2020-style systematic review examining whether
grid digital-twin security research treats AI as a defensive tool faster than it models
AI-enabled threats — or the twin itself — as an attack target.

- **Type:** systematic literature review + research agenda (not an empirical study)
- **Target venue:** *International Journal of Critical Infrastructure Protection* (Elsevier)
- **Corpus:** 100 studies (2020–2026), screened from 1,287 unique OpenAlex records;
  83 coded at full text, 17 at abstract level
- **Status:** manuscript drafted (`manuscript.pdf`); author list is a placeholder pending
  finalisation

---

## Key findings

| Finding | Number |
|---|---|
| AI used **defensively** (full text) | 70 / 83 |
| Engage **any** AI-enabled threat | 35 / 83 (42.2%) |
| Engage an AI threat **substantively** | 11 / 83 (13.3%) |
| Treat the twin itself as an **attack target** | 1 / 83 |
| Research concentrated at **operation** stage | 66 / 83 |
| Studies from **2025–2026** | 76% |

AI-threat engagement by vector (score ≥1): adversarial ML 24, poisoning 19, evasion 9,
LLM 4, agentic 2. The earlier abstract-level screening figure (24/469 = 5.1%) was
removed from the manuscript: its probe-pool denominator is not part of the released
record, so it supported no quantified comparison. The manuscript now states only the
directional point — abstract-level screening under-counts engagement relative to
full-text coding.

Two coders coded a stratified 20% blind sample: κ = 0.60 for "any engagement",
κ = 0.14 for "substantive" engagement (results are stated as bounds, not population
estimates). Full per-field agreement statistics: [`analysis/reliability/AGREEMENT.md`](analysis/reliability/AGREEMENT.md).

---

## Repository layout

```
PAPER_PLAN.md                    paper plan: research questions, contributions, timeline, traps
manuscript.tex                   LaTeX source (elsarticle, IJCIP)
manuscript.pdf                   compiled manuscript
included.bib                     bibliography (101 entries)
highlights.txt                   Elsevier highlights
figures/                         5 figures (PDF + PNG, 300 dpi) and make_figures.py
analysis/
  RESULTS.md                     headline numbers derived from the extraction matrix
  codebook.md                    coding manual — authoritative field definitions
  CODING_INSTRUCTIONS.md         standalone second-coder brief
  COMPETING_REVIEWS.md           novelty check and repositioning decision
  extraction_matrix.csv          the matrix — sole source of every table number
  doi_verification_all.csv       Crossref/DataCite verification of all DOIs
  build_matrix.py                rebuilds the matrix + reliability sample from source CSVs
  verify_all_dois.py             verifies every DOI against Crossref, then DataCite
  reliability/                   agreement stats, coder sheets, disagreement log
  evidence/                      extracted evidence digests
downloads_manifest.csv           retrieval manifest (query set, run dates, outcomes)
digital_twin_grid_cybersecurity_papers.csv   screened corpus with abstracts
doi_verification.csv             DOI verification log
venue_index.csv / prisma_flow.txt            PRISMA flow inputs
*_proposal.pdf/.pptx             research proposal
Peer_Review_Report*.pdf, peerreview*.docx    peer review materials
gen_bib.py                       bibliography helper
```

**Not in this repository:** `papers/` (full-text PDFs, ~311 MB — not redistributable),
`crypto-trader/` (unrelated), and LaTeX build artefacts. See [`.gitignore`](.gitignore).

## Reproducing the analysis

All scripts are plain Python 3 with no CLI arguments; most depend only on the standard
library (`figures/make_figures.py` additionally needs `matplotlib`). Scripts auto-detect
the repository root from their own location, so they run from any working directory;
set `DTGRID_ROOT` to override the root if you relocate the data.

```bash
# 1. Verify every DOI against Crossref, then DataCite
python3 analysis/verify_all_dois.py

# 2. Rebuild the extraction matrix and reliability sample
python3 analysis/build_matrix.py

# 3. Inter-coder agreement on the 20-paper blind sample
python3 analysis/reliability_agreement.py

# 4. Regenerate all five figures (300 dpi, PDF + PNG)
python3 figures/make_figures.py
```

**Important:** `build_matrix.py` emits the matrix with *empty* coding columns — the coded
values in `analysis/extraction_matrix.csv` are the product of human reading against
`analysis/codebook.md`. Do not regenerate the matrix if you want to preserve the coding.

Every number in the manuscript tables is derived from `analysis/extraction_matrix.csv`;
[`analysis/RESULTS.md`](analysis/RESULTS.md) is the readable summary of those derivations.

## Building the manuscript

Requires a LaTeX distribution with `elsarticle` (TeX Live / MiKTeX).

```bash
pdflatex manuscript.tex
bibtex manuscript          # optional: manuscript.bbl is committed
pdflatex manuscript.tex
pdflatex manuscript.tex
```

Figures live in `figures/` and are found via `\graphicspath`.

---

## Method summary

Following PRISMA 2020 style: an OpenAlex query set (including explicit adversarial-AI
probes) yielded 1,287 unique records; title/abstract screening, full-text retrieval, and
DOI verification reduced these to 100 studies that both name a *digital twin* and a
*security term* in a power-grid context. Full texts (83) were coded across 46 fields by
computer-assisted human reading, with a stratified 20% double-coded sample for
reliability. Adversarial-ML grid work that does not mention a twin is out of scope.

**Positioning:** the review is a theory-testing complement to Habeeb, Weli & Almaliki's
(2026) PRISMA review of "Dual-Role Digital Twins", which operationalises only the defence
axis. See [`analysis/COMPETING_REVIEWS.md`](analysis/COMPETING_REVIEWS.md).

## Known caveats

- Full-text claims rest on **83/100** records (17 are abstract-only) — never cite "100"
  for full-text numbers.
- **76% of the corpus is 2025–26**; treat it as a dated snapshot with a stated search
  cutoff.
- Inter-rater κ must be read alongside prevalence; where a category is near-constant,
  percentage agreement is reported instead (see `AGREEMENT.md`).
- Manuscript author list and corresponding author are **placeholders** (the
  Research4Life waiver route constrains the corresponding-author affiliation).

## Licence

Code and analysis scripts are provided for reproducibility alongside the manuscript.
The published papers in `papers/` are **not** included and remain the copyright of their
publishers.


