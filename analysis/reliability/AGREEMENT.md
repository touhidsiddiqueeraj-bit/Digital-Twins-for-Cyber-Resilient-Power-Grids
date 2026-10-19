# Inter-coder agreement — reliability sample

**Design.** Coder 2 independently coded 20 of the 100 papers (20%) using
`CODING_INSTRUCTIONS.md` and a sheet carrying no screening label. C1's codes are the
primary codes in `analysis/coder1_codes.csv`; C2's are in
`analysis/reliability/coder2_sheet.csv`. Both sheets are codebook-valid — a value-by-value
check against the closed vocabularies found no out-of-vocabulary entry (`partial` in
`data_available` and `other` in `ml_role` are both permitted).

Reproduce: `python3 analysis/reliability_agreement.py`.

## Results

Cohen's κ for nominal fields; exact-set match and mean Jaccard for multi-label fields.
`maj%` is the share of the modal category in C1 — when it is ≥90% the κ chance term is
dominated by prevalence and κ is not interpretable.

| field | n | %agree | κ | maj% | reading |
|---|---|---|---|---|---|
| twin_role | 20 | 95% | **0.77** | 90% | substantial |
| baseline_compared | 20 | 95% | **0.90** | 50% | almost perfect |
| ai_poisoning | 20 | 90% | **0.73** | 75% | substantial |
| threat_model_explicit | 20 | 90% | **0.69** | 75% | substantial |
| metrics_reported | 20 | 85% | **0.68** | 60% | substantial |
| security_primary | 20 | 85% | 0.58 | 85% | moderate |
| ml_used | 20 | 85% | 0.57 | 80% | moderate |
| ml_role | 20 | 70% | 0.55 | 45% | moderate |
| stance | 20 | 60% | 0.46 | 45% | moderate |
| dt_type | 20 | 75% | 0.46 | 80% | moderate |
| grid_domain | 20 | 65% | 0.44 | 65% | moderate |
| ai_adv_ml | 20 | 70% | 0.44 | 65% | moderate |
| maturity | 20 | 60% | 0.42 | 60% | moderate |
| ai_threat_overall | 20 | 65% | 0.41 | 55% | fair |
| ai_evasion | 20 | 75% | 0.39 | 85% | fair |
| eval_method | 20 | 50% | 0.37 | 35% | fair |
| lifecycle_stage | 20 | 65% | 0.32 | 80% | fair |
| attack_surface_named | 20 | 60% | 0.14 | 55% | slight |
| ai_llm | 20 | 90% | 0.31 † | 95% | % agreement only |
| ai_agentic | 20 | 95% | 0.00 † | 100% | % agreement only |
| code_available | 20 | 100% | 1.00 † | 95% | % agreement only |
| stance_confidence | 20 | 70% | −0.09 † | 95% | % agreement only |
| limitations_stated | 20 | 70% | −0.15 † | 90% | % agreement only |
| data_available | 20 | 85% | −0.03 † | 90% | % agreement only |
| adversary_adaptive | 20 | 80% | −0.08 | 85% | genuine, low prevalence |
| threat_models_named | 20 | 5% exact | Jaccard 0.43 | — | overlapping lists |
| ml_family | 20 | 20% exact | Jaccard 0.30 (0.42 norm.) | — | free text |
| threat_count | 20 | 10% exact | mean |diff| 1.80 | — | tied to the field above |

† κ is not interpretable: one category ≥90%, so the chance term swamps the statistic. The
reported figure for these is % agreement. A negative κ here (e.g. `limitations_stated`
−0.15) does **not** mean the coders anti-agree; it means the field is near-constant and the
few disagreements run one way.

## What this says

1. **The headline variables hold up.** `twin_role` (κ 0.77) — the field behind the
   "no paper articulates the dual role" result — is substantial. `threat_model_explicit`
   (0.69), `ai_poisoning` (0.73) and `baseline_compared` (0.90) are strong.
2. **`ai_threat_overall` is fair, not strong** (κ 0.41, 65%). The headline percentage
   should be reported with this κ attached. The per-vector AI fields sit in the same band
   (`ai_adv_ml` 0.44, `ai_evasion` 0.39).
3. **A systematic coder style difference explains most of the low scores.** C1 tends to
   assign the dominant/default category (`high`, `yes`, `operation`, `single`); C2
   differentiates more (`medium`, `no`, `multi`, `unclear`) and names more attack surfaces.
   This is the single largest source of disagreement and it is a **codebook** problem, not a
   coder problem: the instructions left the boundary between the default and the exception
   under-specified. Concrete fixes:
   - `lifecycle_stage`: define when a paper spanning design-and-operation is `multi` rather
     than `operation` (7 of 7 disagreements are this boundary).
   - `attack_surface_named`: state the threshold for `yes` (any named entry point vs. a
     substantive attack-surface discussion). 8/8 disagreements are one-directional, C2 more
     inclusive.
   - `stance_confidence`, `limitations_stated`, `data_available`: these are near-constant
     and should be dropped or merged; they carry no discriminative information at this
     corpus size.
   - `ml_family` is free text: contract to the listed vocabulary with `;` separators.
     Normalising names/separators already raises Jaccard 0.30 → 0.42.
4. **Multi-label fields need a set metric, not exact match.** `threat_models_named`
   exact-set agreement is 5% but mean Jaccard is 0.43 — the coders agree on roughly half the
   threat content per paper. Report Jaccard, and state that `threat_count` inherits this
   uncertainty (mean |difference| 1.8 threats).

## Adjudication outcome

The 20-row sample produced **149 field-level disagreements**. Resolved against the codebook
(§10), with `ml_family` contracted to the controlled vocabulary and `threat_models_named`
compared as a set (not a string, which had counted mere reordering as a disagreement):

- **Net cells changed from C1: 20** — `ml_family` 12, `threat_models_named` 2, `stance` 2,
  `eval_method` 2, `dt_type` 1, `grid_domain` 1.
- **Headline AI-threat fields unchanged.** Every `ai_threat_overall` and per-vector disagreement
  was reviewed and resolved to C1's value: the digest shows the alternatives were generated attack
  *data* or LLM/agentic technology used as a **tool**, not an AI-enabled **threat** (e.g. id 21,
  where C2 read multi-agent *defence* as agentic attack automation).
- **Two values were neither coder's:** ids 55 and 62 → `eval_method = hil` (both coders missed the
  hardware-in-the-loop rig; rule R6).
- **Genuine corrections:** ids 22 and 49 → `stance = bridge` (both papers generate adversarial
  attack data / inject attacks into their own twin — codebook §2.1); id 62 → `grid_domain =
  substation`; ids 2 and 43 gained a named threat the digest supports.
- **Not resolvable by rule:** `ml_family` disagrees on content in 14/20 rows even after
  vocabulary contraction (mean Jaccard 0.42). It is a descriptive field only; the adjudicated
  value is the canonical union of both coders and this is stated in the methods.

Codebook revisions R2–R6 (stance review/enabling; attack-surface threshold; lifecycle `multi`
trigger; `ml_family` vocabulary; eval/maturity precedence) absorb the systematic causes. Full
resolution is in `analysis/codes/adjudicated.txt`; `merge_codes.py` applies it and sets
`adjudicated = yes` on the 20 rows in `extraction_matrix.csv`. `coder1_codes.csv` is frozen
before the overlay, so the agreement table above still reflects the two **independent** codings.

## Status

Adjudicated. `extraction_matrix.csv` carries the resolved codes (20 rows `adjudicated = yes`);
the headline percentages in `RESULTS.md` are unchanged because no headline field moved.

