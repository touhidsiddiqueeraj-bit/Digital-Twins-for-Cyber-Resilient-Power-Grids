# Round-8 reliability protocol — the commissioned human check on the headline fields

**Status: pre-specified and released; human execution pending.** The round-7
review required an independent reliability check that this review's own
limitations section names: an independent (non-author) coder, a sample of at
least 50 records enriched for engaged cases, a third-party adjudicator, and an
independent full-text re-read of a random sample of the 48 zero-coded records
with a miss-rate estimate. This file specifies that protocol exactly, so that
its execution is a matter of staffing rather than design. What was executable
without human coders — an independent automated (LLM-instrument) readback at
abstract-plus-window level over all 83 full-text records — was carried out and
is reported in the manuscript (Sections 4.8, 5.7, 5.8) and released as
`analysis/reliability/readback_ai_codes.csv` (per-record codes and
quoted bases) and `analysis/reliability/readback_joined.csv` (joined
against coder 1). The automated readback substitutes a reader, not the
evidence base: it reads released keyword windows and stored/fetched abstracts,
so it cannot catch misses that window selection would not contain, and it does
not replace this protocol.

## 1. Coders and independence

- **Coder A (independent):** a researcher outside the author team, with no
  role in corpus assembly or coding, trained on `analysis/CODING_INSTRUCTIONS.md`
  and the codebook (`analysis/codebook.md`), blind to coder 1's values, to the
  screening label, and to the review's headline figures.
- **Adjudicator:** a third party (e.g., a methods-literate colleague not
  otherwise involved), who receives the disagreement list only, resolves each
  cell against the codebook and evidence, and does *not* default to either
  coder. The tie-break rule is documented per cell.

## 2. Sample

- **Frame:** the 83 full-text-coded records.
- **Enriched sample, n = 60:** all 35 records coded as engaging an AI-enabled
  threat (any level) plus a seeded uniform random sample of 25 of the 48
  zero-coded records (seed 11; ids to be fixed at execution time and released).
  Enrichment guarantees positive-class information, which the round-4 sample
  (about 9 positives in 20) lacked.
- **Fields coded:** `ai_threat_overall` (0/1/2), `attack_surface_named`,
  `twin_role`, and the round-8 direction field
  (`ai_direction`: attacks on AI components / attacks wielded with AI /
  both / unclear), applied per record to each engaged vector.

## 3. Negatives re-read

- **Full-text re-read of a random sample of 20 of the 48 zero-coded records**
  (seed 11), reading the obtained full texts — not abstracts, not windows —
  and recording any engagement that the coding missed.
- **Miss-rate estimate:** k/20 with a Wilson 95% interval, propagated to the
  headline as (35 + 48·k/20) of 83, reported alongside the 35/83 point value.

## 4. Analysis

- Per-field: percentage agreement, Cohen's κ with bootstrap 95% CI (2,000
  resamples), PABAK, Gwet's AC1, and the bias index, computed by extending
  `analysis/reliability_round4.py` / `analysis/reliability_agreement.py`.
- Comparisons: coder A vs coder 1; coder A vs coder 2 on the original
  20-record sample; and the three-way disagreement list, adjudicated cell by
  cell.
- **Failure conditions, stated in advance:** the any-level headline (35/83)
  is treated as fragile if the independent any-collapse κ < 0.4 or if the
  negatives re-read miss-rate exceeds 15% (Wilson lower bound above 5%);
  the substantive tier (11/83) is treated as unreportable as a count if the
  independent substantive-collapse κ < 0.2.

## 5. What the automated round-8 readback already provides (and does not)

- Provides: a third, non-author judgment on all 83 records from released
  evidence, with per-record quoted bases; a negatives census (all 48, not a
  sample) with a miss-rate estimate (2/48 = 4.2%, Wilson 95% CI 1.2–14.0%);
  confirmation that the two flagged borderline records of round 7 (R21, R100)
  are the only score-1 candidates the window evidence supports (plus R44);
  and a coded direction field for all 35 engaged records.
- Does not provide: independence from the window-selection process (the
  evidence base is shared with the extraction), human-judgment validity for
  the substantive threshold (windows cannot evidence "a section dedicated to
  it"), or any test of the 17 abstract-only records.
