# Search snapshot — reconstructed strings, dated Crossref run

**Run date: 2026-10-19. Status: strings are RECONSTRUCTIONS, not the originals.**

The original 16 OpenAlex query strings (12 core + 4 adversarial-AI probes) were not
preserved in the released record (see `../../SEARCH_PROVENANCE.md`). The strings in
`queries.json` were reconstructed from the method description: each core query
combines a digital-twin term, a grid-domain term and a security term; the four probes
combine digital-twin + grid terms with adversarial-ML, poisoning, evasion and
LLM terms, matching the probe topics named in the manuscript.

- **OpenAlex re-run: attempted 2026-10-19, blocked.** The API returned
  "Insufficient budget" for the shared-IP free tier (resets at midnight UTC), so the
  original 1,287-record pool cannot be regenerated in this session. A re-run with an
  API key, plus per-record provenance, remains the required artifact.
- **Second database: Crossref.** Each query was run against
  `api.crossref.org/works?query.bibliographic=...` on 2026-10-19; the top-100
  relevance-ordered results per query are archived as `core-01.csv` ... `probe-04.csv`.
- **Crossref total-results are NOT comparable to the OpenAlex pool sizes.** Crossref
  `query.bibliographic` is a fuzzy relevance search over all registered works; the
  totals count everything that weakly matches. The archived value of this snapshot is
  the frozen strings + the per-query result lists + the run date, so that a future
  re-run (OpenAlex and/or Crossref) has a dated reference point, not the totals.
