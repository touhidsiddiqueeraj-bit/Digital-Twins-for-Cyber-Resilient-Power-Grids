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
- **Status:** revised through six review rounds (3–8); point-by-point responses in
  `REVIEW_RESPONSE.md`. Author list is a placeholder pending finalisation

---

## Key findings

| Finding | Number |
|---|---|
| ML used (full text) | 70 / 83 — **for detection in 55** (forecasting 12, control 3 are not security functions) |
| Engage **any** AI-enabled threat | 35 / 83 (42.2%); strict grid scope 33/79; a majority in the core subsets (16/29, 30/55) — the corpus was retrieved with defensive vocabulary and the round-8 reconstruction shows the probe channel contributed at most one record (R50), so rates describe the core-vocabulary, defensively-framed literature only |
| Engage an AI threat **substantively** | 11 / 83 (13.3%; strict scope 10/79) — on the weakest coder collapse (κ = 0.14) and a threshold that partly proxies document length (0/14 conference papers; 9/62 journals, so minority within the dominant format too): **depth is not reliably measured by this instrument**; the misclassification interval 21–51 of 83 spans minority and majority readings |
| Direction of engagement (round-8 coded field) | 25 of the 35 engaged records acknowledge attacks **on** AI components; 6 wield AI **with** hostile intent (R2, R49, R57, R64, R69, R84); 2 both; 2 unclear — engagement is mostly defender-framed vulnerability acknowledgment |
| Twin as the adversary's **objective** (strict) | **0 grid studies** — a domain-scoped descriptive observation: 1 non-grid vehicle record; 56/83 name interface or model threats in a defender frame (tool is the near-constant default, 75/83); and the two read nuclear-domain records (R91, R92 — `analysis/R7_READBACK.md`) do attack twin interfaces and twin ML models, so the unqualified claim is gone |
| Research concentrated at **operation** stage | 66 / 83 (lifecycle κ = 0.32, AC1 0.54 — descriptive only; the single design-phase record is out-of-domain) |
| Studies from **2025–2026** | 76% — a recency-heavy corpus profile (IDs 1–45 all 2026, 40/100 zero-citation; per-record counts in Appendix A's Cit. column). The ranking manifest (`analysis/search_snapshot_2026-10-19/round8/retained100_ranking_manifest.csv`) verifies the display-order claim; the dated Crossref reconstruction shows the eligible pool is itself 66.7% 2025+, so the cut amplified but did not manufacture the recency profile |

AI-threat engagement by vector (score ≥1): adversarial ML 24, poisoning 19, evasion 9,
LLM 4, agentic 2. The previously quoted abstract-level figure (24/469) was an
unreproducible working number from an unpreserved scan and has been deleted from the
manuscript. Round-7 readbacks (15 weak audit firings inspected; seeded 12-record sample
of the 48 negatives re-read; R91/R92 obtained and read) are documented in
`analysis/R7_READBACK.md`; no substantive false negative was found. **Round 8 adds an
independent automated (LLM) readback of all 83 full-text records**
(`analysis/reliability/round8_ai_readback_codes.csv`): any-collapse agreement with
coder 1 79/83 (κ = 0.90), five informative disagreements (R32/R66 plan-only; R44/R100
one-liners; R55 suspected-substantive), and a negatives census whose miss-rate is 2/48
= 4.2% (Wilson 95% CI 1.2–14.0%) — the readback upper bound for any-level engagement
remains 37/83 (44.6%). The commissioned human protocol (non-author coder, ≥50 enriched,
third-party adjudicator, full-text negatives re-read) is pre-specified in
`analysis/reliability_protocol_round8.md`, staffing pending.

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
PAPER_PLAN.md                    paper plan: research questions, contributions, timeline, traps
manuscript.tex                   LaTeX source (elsarticle, IJCIP)
manuscript.pdf                   compiled manuscript
appendix_corpus.tex              Appendix A: all 100 studies, with Cit. column (gen_appendix.py)
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
  reliability/                   agreement stats, coder sheets, disagreement log,
                                 round-8 independent readback codes + joined comparison
  evidence/                      extracted evidence digests
  R7_READBACK.md                 round-7 readbacks: 15 weak firings, negatives sample, R91/R92 coding
  round7_stats.py                round-7 sensitivities (cited/uncited, venue-length, overlaps)
  reliability_protocol_round8.md pre-specified human reliability protocol (staffing pending)
  quality_appraisal_round8.csv   round-8 light quality signals (peer venue, cited, eval, repro)
  round8_*.py                    round-8 computations: provenance, retrievability, term
                                 breakdown, evidence dump, reliability, stats (items 1,3-9)
  search_snapshot_2026-10-19/
    round8/                      dated Crossref reconstruction (README inside): per-record
                                 query provenance, probe-only finding, probe-added screening,
                                 ranking manifest, eligible-export re-execution, term breakdown
downloads_manifest.csv           retrieval manifest (query set, run dates, outcomes)
digital_twin_grid_cybersecurity_papers.csv   screened corpus with abstracts
doi_verification.csv             DOI verification log
venue_index.csv / prisma_flow.txt            PRISMA flow inputs
SEARCH_PROVENANCE.md             search-provenance gap manifest (required artifacts)
REVIEW_RESPONSE.md               point-by-point responses to the round-3–7 reviews
*_proposal.pdf/.pptx             research proposal
habeeb2026_dual_role_digital_twins.pdf      Habeeb et al. (2026), the closest prior review
reviews/                         peer review materials (rounds 1–2, consistently named)
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
  candidate pool but cannot be shown to have contributed to the retained 100; the claim
  that they make the result robust to retrieval bias is withdrawn. See
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


