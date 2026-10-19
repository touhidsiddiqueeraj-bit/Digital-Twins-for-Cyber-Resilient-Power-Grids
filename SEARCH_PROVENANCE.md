# Search provenance manifest — what is released, what is missing, what must be released

**Status: PARTIALLY RESOLVED BY DATED RECONSTRUCTION (2026-10-19, round 8); original
OpenAlex provenance remains unrecoverable.** This file exists because the round-3 review
established that the four adversarial-AI probe queries cannot be shown to have
influenced the corpus. Round 7 declared the gap; round 8 re-executed the query semantics
against Crossref to a depth of 1,000 results per query and released the reconstruction
(`analysis/search_snapshot_2026-10-19/round8/`, README therein). The reconstruction
answers the probe question (at most one retained record, R50, is probe-only) and
establishes a dated screening status for the probe-added channel; it does not and cannot
recover the original OpenAlex strings, run dates or per-record provenance, which remain
the required artifacts listed below.

## What happened

- Twelve core OpenAlex queries (digital-twin term × grid-domain term × security term)
  returned **1,287** unique records. This is the screened set: 795 failed the three-term
  eligibility rule, leaving **492 eligible**, of which the **top 100** were retained by a
  declared non-probabilistic ranking (relevance, citations, recency).
- Four adversarial-AI probe queries (digital-twin + grid terms × adversarial ML /
  poisoning / evasion / LLM terms) raised the candidate pool to **≈2,000** records.
- **The released record does not establish how many of the 492 eligible records, or of
  the retained 100, are retrievable only through the probes.** Per-record query
  provenance was not retained, and the query strings themselves are not in the
  repository.

## Why it matters

The probes were added to defend the headline (shallow attack-side engagement) against
retrieval bias: the core grid-security vocabulary is not expected to retrieve attack-side
literature. If no probe-only record entered the retained corpus, the corpus derives from
the core vocabulary alone — which is exactly the retrieval bias the probes were meant to
fix — and the measured asymmetry may be overstated relative to the un-retrieved
attack-side literature. The manuscript (Methods §4.2, Discussion §6.5, Threats to
Validity §8.5) states this and makes no retrieval-bias defence for the probes.

## Artifacts that must be released to resolve it

1. **The 16 query strings** (12 core + 4 probes), verbatim, in OpenAlex syntax.
   *Partial (2026-10-19):* reconstructed strings are archived in
   `analysis/search_snapshot_2026-10-19/` together with a dated Crossref
   (second-database) run of each — extended in round 8 to the top-1,000 results per
   query (`round8/top1000/`); the **originals** remain unreleased. OpenAlex re-runs were
   attempted **three times** on 2026-10-19 (twice in round 7, once during the round-8
   revision) and blocked each time by the shared-IP API budget (`Rate limit exceeded —
   insufficient budget`). Re-running the search with logged queries remains the
   prerequisite for any attack-side claim about the literature.
2. **Run dates** for each query, and the OpenAlex snapshot semantics (citation counts
   and relevance scores are date-dependent).
3. **Per-record query provenance**: for every record in the candidate pool (≈2,000),
   the set of queries that returned it, keyed by OpenAlex work ID and DOI.
   *Round-8 reconstruction:* `round8/provenance_retained100.csv` (top-1,000 list match)
   and `round8/retrievability_textlevel.csv` (phrase-component re-execution against
   each retained record's own title/abstract/windows) provide this per retained record
   on the dated Crossref pool; the original OpenAlex provenance is not recoverable.
4. **The full candidate pool export** (all fields), not only the 1,287 screened or the
   100 retained, so the 392 eligible-but-not-retained records are visible and the
   ranking rule can be re-executed.
   *Round-8 reconstruction:* `round8/core_eligible_export.csv` re-executes the pipeline
   on the dated Crossref pool (5,179 unique core-list records → 192 eligible → ranked
   → cut at 100), and `round8/retained100_ranking_manifest.csv` releases the ranking
   components of the realised corpus. The original 492-record export remains
   unrecoverable.
5. **A re-run of the headline on the probe-only subset**: among the retained 100 (and
   among the 492), how many are probe-only, and what is the AI-threat engagement rate
   in that subset versus the core-only subset.
   *Round-8 outcome:* at most one retained record (R50) is probe-only under either
   reconstruction; the probe-only subset of the full-text corpus has n ≤ 1 (R50,
   substantive), so the headline is a measurement of core-retrievable records.
   Additionally, `round8/probe_added_screening.csv` and
   `round8/probe_added_term_breakdown.csv` establish the dated screening status of the
   probe-added channel: 1,484 probe-added candidates, 14 eligible, none carrying
   adversarial-AI vocabulary — of the 396 that do carry it, only 59 name a digital
   twin, and only 4 name a digital twin together with a grid term. The three-term
   eligibility rule is itself an attack-side filter.

## Reproducibility note (ranked subset)

Even with the above released, the retained 100 remain a **ranked subset**, not a random
sample of the 492 eligible records. Prevalence figures in the manuscript describe the
retained corpus. A defensible upgrade path, stated in the review response, is to
double-code a **random** sample of the 492 (or all 492 on abstract-level fields) and
report the headline on that frame; the current package does not contain the 492-record
export needed to do this.

## File inventory (search-related, currently released)

| File | Contents | Provenance coverage |
|---|---|---|
| `digital_twin_grid_cybersecurity_papers.csv` | the 100 retained records + abstracts | none (no query column) |
| `downloads_manifest.csv` | retrieval manifest for the 100 | bucket/src/type only, no query |
| `prisma_flow.txt` | flow counts (1,287 / 795 / 492 / 100) | aggregate only |
| `venue_index.csv` | venue→bucket mapping for downloads | none |
| `paywalled_dois.csv`, `free_blocked_download_links.csv` | non-retrieved full texts | none |
| `analysis/search_snapshot_2026-10-19/round8/*.csv` | dated Crossref reconstruction: per-record query provenance (retained 100), probe-added screening, ranking manifest, eligible-export re-execution, term breakdown | second-database proxy, dated 2026-10-19; not the original OpenAlex provenance |

None of the original-pool files carries per-record query provenance; the round-8
files carry it for the retained 100 on the dated reconstruction.

## Related figure with the same provenance problem (deleted)

The abstract-level screening figure quoted in earlier drafts ("24 of 469 records,
5.1%") derives from an earlier probe-relevance scan whose **per-record artifact was not
preserved**. Its relation to the ≈700 probe-added candidates is not established in the
released record. Following the round-7 review, the figure and the speculation attached
to it have been **deleted from the manuscript entirely** rather than discussed as if it
were evidence; no per-record abstract-level screening artifact survives.

## Full-text retrieval attempts for R91 and R92 (2026-10-19, round 7)

- **R91** (Spirito, Ly & Veretennikov 2023, INL/RPT-23-75113, DOI 10.2172/2337610):
  the OSTI full-text endpoint (`osti.gov/servlets/purl/2337610`) was unreachable from
  this environment (connection failure on direct fetch; fetch layer also failed on the
  PDF). The full text (48 pp.) was retrieved from the INL digital library
  (`inldigitallibrary.inl.gov/sites/sti/sti/Sort_74726.pdf`) and read; coding in
  `analysis/R7_READBACK.md`. The PDF is not redistributed with the package.
- **R92** (Spirito, Zhang & Hossain 2023, INL/RPT-23-75114, DOI 10.2172/2331253):
  two full-text retrieval attempts failed (OSTI purl unreachable; no mirror found via
  the INL library or Semantic Scholar, both of which point back to OSTI). The report's
  extended abstract was obtained from the OSTI record and read; the coding rests on it
  and is disclosed as abstract-based wherever used.
