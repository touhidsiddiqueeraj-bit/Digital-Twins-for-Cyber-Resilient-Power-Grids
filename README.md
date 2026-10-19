# Digital Twins for Cyber-Resilient Power Grids

**A Structured Corpus Review of AI Use, Threat Engagement, and Measurement Limits**

Code, data, and manuscript for a structured literature review (PRISMA-flow reporting on a
ranked corpus — not a PRISMA systematic review) measuring how grid digital-twin security
research uses AI defensively and engages AI-enabled threats — and the twin itself — as
attack objects. The original asymmetry hypothesis (defensive use common, attack-side
engagement rare) was not supported; the review reports the narrower, instrument-bounded
finding: any-level engagement is common in this corpus, and depth is not reliably measured
by the coding instrument.

- **Type:** structured literature review + research agenda (not an empirical study; not a
  registered systematic review — one database, ranked top-100 subset)
- **Target venue:** *International Journal of Critical Infrastructure Protection* (Elsevier)
- **Corpus:** 100 studies (2020–2026), a declared non-probabilistic top-100 ranking of 492
  eligible records screened from 1,287 unique OpenAlex core-query records;
  83 coded at full text, 17 at abstract level
- **Status:** manuscript complete; author list is a placeholder pending finalisation

---

## Key findings

| Finding | Number |
|---|---|
| ML used (full text) | 70 / 83 — **for detection in 55** (forecasting 12, control 3 are not security functions) |
| Engage **any** AI-enabled threat | 35 / 83 (42.2%); a majority in the core subsets (16/29, 30/55) — but the corpus was retrieved with defensive vocabulary, so rates describe the defensively-framed literature only |
| Engage an AI threat **substantively** | 11 / 83 (13.3%) — on the weakest coder collapse (κ = 0.14, 1 of 6 positives doubly agreed) and a threshold that partly proxies document length (0/14 conference papers clear it): **depth is not reliably measured by this instrument**; the misclassification interval 21–51 of 83 spans minority and majority readings |
| Twin as the adversary's **objective** (strict) | **0 grid studies** — a domain-scoped descriptive observation: 1 non-grid vehicle record; 56/83 name interface or model threats in a defender frame (tool is the near-constant default, 75/83); and the two read nuclear-domain records (R91, R92 — `analysis/READBACK.md`) do attack twin interfaces and twin ML models, so the unqualified claim is gone |
| Research concentrated at **operation** stage | 66 / 83 (lifecycle κ = 0.32, AC1 0.54 — descriptive only; the single design-phase record is out-of-domain) |
| Studies from **2025–2026** | 76% — a recency-heavy corpus profile (IDs 1–45 all 2026, 40/100 zero-citation; per-record counts in Appendix A's Cit. column). Which ranking component dominated is not recoverable from the released record; the clean test needs the year distribution of the 492 eligible vs the retained 100 |

AI-threat engagement by vector (score ≥1): adversarial ML 24, poisoning 19, evasion 9,
LLM 4, agentic 2. The abstract-level screening figure (24/469) from an unpreserved
probe-relevance scan is an unreproducible working number and is not used in the
manuscript. The post-hoc readback audit (15 weak audit firings inspected; seeded 12-record
sample of the 48 negatives re-read; R91/R92 obtained and read) is documented in
`analysis/READBACK.md`; no substantive false negative was found, and the readback
upper bound for any-level engagement is 37/83 (44.6%).

Two coders (both authors of the review) coded a blind sample of 20 of the 83 full-text
records (24%): κ = 0.60 (bootstrap 95% CI 0.20–0.90) for "any engagement", κ = 0.14
(−0.23–0.64) for "substantive", linear weighted κ = 0.43 and Gwet's AC1 = 0.50 on the
three-level scale, plus PABAK, bias indices and a per-field AC1 column. Family-level
threat-vocabulary agreement (interface κ = 0.70, classical 85%, learned-model κ = 0.37)
replaces exact-set matching as the quotable vocabulary statistic. A
misclassification sensitivity anchored on the second coder puts the headline at 36/83
(95% CI 21–51). Full per-field agreement statistics:
[`analysis/reliability/AGREEMENT.md`](analysis/reliability/AGREEMENT.md).

---

## Repository layout

```
manuscript.tex                   LaTeX source (elsarticle, IJCIP)
manuscript.pdf                   compiled manuscript
appendix_corpus.tex              Appendix A: all 100 studies, with Cit. column (gen_appendix.py)
included.bib                     bibliography (107 entries)
highlights.txt                   Elsevier highlights
figures/                         5 figures (PDF + PNG, 300 dpi) and make_figures.py
analysis/
  RESULTS.md                     headline numbers derived from the extraction matrix
  codebook.md                    coding manual — authoritative field definitions
  CODING_INSTRUCTIONS.md         standalone second-coder brief
  COMPETING_REVIEWS.md           novelty check against the closest prior review
  extraction_matrix.csv          the matrix — sole source of every table number
  doi_verification_all.csv       Crossref/DataCite verification of all DOIs
  build_matrix.py                rebuilds the matrix + reliability sample from source CSVs
  verify_all_dois.py             verifies every DOI against Crossref, then DataCite
  reliability/                   agreement stats, coder sheets, disagreement log
  evidence/                      extracted evidence digests
  READBACK.md                    post-hoc readback audit: 15 weak firings, negatives sample, R91/R92 coding
  sensitivities.py               sensitivity analyses (cited/uncited, venue-length, overlaps)
downloads_manifest.csv           retrieval manifest (query set, run dates, outcomes)
digital_twin_grid_cybersecurity_papers.csv   screened corpus with abstracts
doi_verification.csv             DOI verification log
venue_index.csv / prisma_flow.txt            PRISMA flow inputs
SEARCH_PROVENANCE.md             search-provenance gap manifest (required artifacts)
*_proposal.pdf/.pptx             research proposal
habeeb2026_dual_role_digital_twins.pdf      Habeeb et al. (2026), the closest prior review
gen_bib.py                       bibliography helper
gen_appendix.py                  Appendix A generator; self-checks the ID-order claims
```

**Not in this repository:** `papers/` (full-text PDFs, ~311 MB — not redistributable),
`crypto-trader/` (unrelated), and LaTeX build artefacts. See [`.gitignore`](.gitignore).

## Reproducing the analysis

All scripts are plain Python 3 with no CLI arguments; most depend only on the standard
library (`figures/make_figures.py` additionally needs `matplotlib`). Scripts resolve the
repository root relative to their own location, so they can be run from a fresh clone.
(`analysis/audit_false_negatives.py` additionally needs the local `papers/` full texts,
which are not redistributable.)

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

Requires a LaTeX distribution with `elsarticle` (TeX Live / MiKTeX), or `tectonic`
(one-pass, fetches packages itself).

```bash
pdflatex manuscript.tex
bibtex manuscript          # required: manuscript.bbl is generated at build time and not committed
pdflatex manuscript.tex
pdflatex manuscript.tex

# or, with tectonic (handles bibtex internally):
tectonic manuscript.tex
```

Figures live in `figures/` and are found via `\graphicspath`.

---

## Method summary

A structured review with PRISMA-2020 flow reporting: twelve OpenAlex core queries
(digital-twin × grid × security terms) yielded 1,287 unique records; title/abstract
screening against the three-term rule left 492 eligible; a declared non-probabilistic
ranking (relevance, citations, recency) retained the top 100. Full texts (83) were coded
across 46 fields by computer-assisted human reading, with a 20-record blind sample
(24% of full-text records) double-coded for reliability (κ, bootstrap CIs, PABAK, bias
indices). Four adversarial-AI probe queries widened the candidate pool to ≈2,000 but
their contribution to the corpus is not established in the released record — declared in
the paper and tracked in `SEARCH_PROVENANCE.md`. Adversarial-ML grid work that does not
mention a twin is out of scope.

**Positioning:** the review is a narrow grid-side measurement (strict twin-as-objective
count, plus looser tiers) complementing Habeeb, Weli & Almaliki's (2026) review of
"Dual-Role Digital Twins". See
[`analysis/COMPETING_REVIEWS.md`](analysis/COMPETING_REVIEWS.md).

## Known caveats

- **This is not a systematic review.** One database, no registered protocol, and a ranked
  (non-random) top-100 subset of 492 eligible records. Prevalence figures describe the
  corpus, not the literature. The title and methods say so.
- **Probe provenance is unresolved.** The four adversarial-AI probe queries widened the
  candidate pool but cannot be shown to have contributed to the retained 100, so no
  retrieval-bias robustness claim is made for them. See
  [`SEARCH_PROVENANCE.md`](SEARCH_PROVENANCE.md) for the gap and the required artifacts.
- Full-text claims rest on **83/100** records (17 are abstract-only) — never cite "100"
  for full-text numbers. The 17% is an access limitation of the authors, not a
  reproducibility finding.
- **76% of the corpus is 2025–26**, partly an artefact of the recency-weighted ranking.
- Inter-rater κ must be read alongside prevalence; PABAK and bias indices are reported
  alongside κ, and the threat-vocabulary fields are the least reliable data in the
  package (exact-set agreement 5%, Jaccard 0.43).
- Manuscript author list and corresponding author are **placeholders** (the
  Research4Life waiver route constrains the corresponding-author affiliation).

## Licence

Code and analysis scripts are provided for reproducibility alongside the manuscript.
The published papers in `papers/` are **not** included and remain the copyright of their
publishers.


