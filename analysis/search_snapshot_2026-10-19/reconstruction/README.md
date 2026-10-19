# Round-8 retrieval-provenance reconstruction — what is here, and what it is not

**Run date: 2026-10-19. Status: dated Crossref reconstruction; the original
OpenAlex provenance remains unrecoverable.**

The original 16 OpenAlex query strings, their run dates, and per-record query
provenance were not preserved (see `../../SEARCH_PROVENANCE.md`). A third
OpenAlex re-run was attempted during this revision and was blocked again by
the shared-IP free-tier budget ("Insufficient budget", 2026-10-19). What this
directory releases is therefore a *second-database reconstruction*, executed
end-to-end on 2026-10-19 with the reconstructed query strings of
`../queries.json`, and it is labelled as such everywhere the manuscript uses
it. It resolves the *shape* of the retrieval question; it cannot certify the
original retrieval.

## Contents

| Path | What it is |
|---|---|
| `top1000/{core,probe}-XX.csv` | Top-1000 Crossref relevance results per query (16 files), with title, abstract where Crossref carries one, year, citation count |
| `provenance_retained100.csv` | Per retained record: which of the 16 top-1000 lists contain it (DOI match, title fallback), membership class (core_only / probe_only / both / not_matched) |
| `retrievability_textlevel.csv` | Per retained record: which queries' phrase components occur in its own title+abstract (variant A) and additionally in the released full-text keyword windows (variant B), with membership class per variant |
| `retained100_crossref_metadata.csv` | Per-DOI Crossref metadata for the retained 100 (full abstracts where deposited) |
| `retained100_ranking_manifest.csv` | The ranking components of the realised corpus: OpenAlex relevance score, citation count at retrieval, year, per retained record (verifies the display-order claim year-desc, citations-desc-within-year) |
| `core_eligible_export.csv` | Dated reconstruction of the eligible pool: the 12 core top-1000 lists merged, de-duplicated, screened with the review's three-term rule (192 records), with best-rank / citations / year ranking manifest and a re-executed top-100 cut |
| `probe_added_screening.csv` | The probe-added pool (probe lists minus core lists, 1,484 records), screened with the three-term rule, with AI-attack vocabulary flags |
| `probe_added_term_breakdown.csv` | Per probe-added record: which of the three eligibility terms (digital-twin / grid / security) its title+abstract carries — decomposing where the attack-side literature is lost between retrieval and eligibility |

Scripts (in `analysis/`): `round8_provenance.py`, `round8_crossref_metadata.py`,
`round8_retrievability.py`, `round8_term_breakdown.py`.

## Headline findings carried into the manuscript (all dated reconstructions)

1. **The probe channel demonstrably did not shape the corpus.** Across both
   reconstructions — top-1000 list match and text-level phrase re-execution —
   at most one retained record (R50) is probe-only; under the generous
   text-level variant (title+abstract+released windows) none is. The probe-only
   subset of the 83 full-text records therefore has n ≤ 1 and cannot move the
   headline; the corpus is a core-vocabulary corpus on this evidence.
2. **The eligibility rule, not only the query, is the attack-side filter.**
   Of the 1,484 probe-added candidates, 396 carry AI-attack vocabulary in
   title/abstract — and none of those passes the review's three-term
   eligibility rule; only 59 of them even name a digital twin, and only 4 name
   a digital twin together with a grid term. The 14 probe-added records that
   do pass eligibility carry no AI-attack vocabulary. Attack-side work that
   does not already self-describe as digital-twin + grid + security is
   invisible to this design by construction.
3. **The top-100 cut is now re-executable end-to-end on a dated pool.** The
   192-record reconstructed eligible export, its ranking manifest
   (best relevance rank, citations, year) and a documented composite cut are
   released; re-executing the cut today retains 27 of the original 100. The
   original 492-record export remains unrecoverable.
4. **The year-distribution "clean test" (Section 4.3) runs on the
   reconstruction.** The reconstructed eligible pool is itself recency-heavy
   (66.7% of records from 2025 onward), against the retained corpus's 76%
   from 2025–26: the corpus's recency concentration is only about nine
   points above the eligible-pool base rate on this evidence, so the top-100
   cut did not manufacture the recency profile, though it amplified it.

## Caveats, stated once

Crossref `query.bibliographic` is a fuzzy relevance search; the top-1000
lists are today's ordering, not OpenAlex's original pool; 47 of the retained
records have no Crossref abstract (title-only evidence in variant A); 11
retained DOIs (Zenodo, OSTI, arXiv — DataCite DOIs) are not in Crossref at
all and were matched on stored titles. None of these caveats weakens finding
2, which depends only on what the probe lists *contain*, not on how complete
they are.
