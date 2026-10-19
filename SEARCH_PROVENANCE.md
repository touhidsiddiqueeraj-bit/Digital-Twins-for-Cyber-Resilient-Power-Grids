# Search provenance manifest — what is released, what is missing, what must be released

**Status: GAP DECLARED (2026-10-19).** This file exists because the round-3 review
established that the four adversarial-AI probe queries cannot be shown to have
influenced the corpus. This manifest records that fact and specifies the artifacts
whose release would resolve it.

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
Validity §8.5) states this and withdraws the earlier claim that the probes make the
result robust.

## Artifacts that must be released to resolve it

1. **The 16 query strings** (12 core + 4 probes), verbatim, in OpenAlex syntax.
   *Partial (2026-10-19):* reconstructed strings are archived in
   `analysis/search_snapshot_2026-10-19/` together with a dated Crossref
   (second-database) run of each; the **originals** remain unreleased. An OpenAlex
   re-run was attempted on 2026-10-19 and blocked by the shared-IP API budget.
2. **Run dates** for each query, and the OpenAlex snapshot semantics (citation counts
   and relevance scores are date-dependent).
3. **Per-record query provenance**: for every record in the candidate pool (≈2,000),
   the set of queries that returned it, keyed by OpenAlex work ID and DOI.
4. **The full candidate pool export** (all fields), not only the 1,287 screened or the
   100 retained, so the 392 eligible-but-not-retained records are visible and the
   ranking rule can be re-executed.
5. **A re-run of the headline on the probe-only subset**: among the retained 100 (and
   among the 492), how many are probe-only, and what is the AI-threat engagement rate
   in that subset versus the core-only subset.

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

None of these files carries per-record query provenance.

## Related figure with the same provenance problem

The abstract-level screening figure quoted in earlier drafts ("24 of 469 records,
5.1%") derives from an earlier probe-relevance scan whose **per-record artifact was not
preserved**. Its relation to the ≈700 probe-added candidates is not established in the
released record, and the manuscript (§5.5, §8.2) now treats it as an unreproducible
working number rather than evidence.
