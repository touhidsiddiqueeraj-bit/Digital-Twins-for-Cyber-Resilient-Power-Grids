# Results — derived from extraction_matrix.csv

Corpus: **100** records; full text **83**, abstract-only **17**.

## Headline: engagement with AI-enabled threats

Full-text records only (n=83). Scale 0 = not addressed, 1 = mentioned/peripheral, 2 = substantive.

| Vector | 0 | 1 | 2 | any (>0) | any % |
|---|---|---|---|---|---|
| any AI-enabled threat | 48 | 24 | 11 | 35 | 42.2% |
| adversarial ML | 59 | 16 | 8 | 24 | 28.9% |
| ML evasion | 74 | 8 | 1 | 9 | 10.8% |
| data/model poisoning | 64 | 12 | 7 | 19 | 22.9% |
| LLM-specific threats | 79 | 2 | 2 | 4 | 4.8% |
| agentic attack automation | 81 | 1 | 1 | 2 | 2.4% |

- Papers engaging **any** AI-enabled threat at all (score ≥1): **35/83 = 42.2%**
- Papers engaging **substantively** (score 2): **11/83 = 13.3%**
- Papers with **no** engagement (score 0): **48/83 = 57.8%**

Abstract-only records (n=17) cannot be coded on these fields; the 17 excluded records are
reported as a limitation, and the abstract-level screening figure (24/469 = 5.1%) was
computed over the wider relevant set, not this corpus.

- Non-grid rows flagged in notes (fraud, vehicle and generic-ICS cases): 4

### Coder 1 stance vs the OpenAlex screening seed

The seed came from title/abstract screening; the coder-1 column is a read of the paper. A large
shift here is a finding about screening, not a coding error, and must be reported.

| Stance | seed (screening) | coder 1 |
|---|---|---|
| adversarial | 11 | 2 |
| defensive | 42 | 42 |
| bridge | 9 | 10 |
| review | 23 | 36 |
| enabling | 15 | 10 |

## Stance

| Stance | all 100 | full text | abstract-only |
|---|---|---|---|
| adversarial | 2 | 1 | 1 |
| defensive | 42 | 32 | 10 |
| bridge | 10 | 8 | 2 |
| review | 36 | 34 | 2 |
| enabling | 10 | 8 | 2 |

- security_primary = yes: **83/100**
- stance_confidence low (escalate to adjudication): ['27', '70']

## The dual-role question (twin_role, full text n=83)

- target: 1
- tool: 75
- unclear: 7

Twin-as-target or both, i.e. the tension the framing addresses: **1/83 = 1.2%**

## Lifecycle stage (full text n=83) — the competitor's first named gap

- design: 1
- multi: 12
- operation: 66
- unclear: 4

Operation-only share: **79.5%**; design or commissioning addressed at all: **1** records.

## Threat vocabulary (full text n=83)

| Threat | records naming it |
|---|---|
| dos | 49 |
| fdi | 46 |
| malware | 34 |
| mitm | 26 |
| replay | 23 |
| false_command | 22 |
| poisoning | 22 |
| physical | 21 |
| insider | 20 |
| supply_chain | 19 |
| evasion | 11 |
| reverse_pathway | 10 |

- Records naming **no** threat at all: **10/83**
- Mean distinct threats named: **3.77**; median 3; max 11

- Adversary modelled as adaptive: **10/83**
- Formal threat model present: **19/83**

## Machine learning (full text n=83)

- Uses ML/AI at all: **70/83**
- ml_role: {'detection': 55, 'forecasting': 12, 'none': 13, 'control': 3}

## Evaluation and rigour (full text n=83)

- eval_method: {'qualitative': 28, 'mixed': 5, 'simulation': 33, 'conceptual': 5, 'testbed': 10, 'hil': 2}
- maturity: {'concept': 34, 'validated': 3, 'prototype': 46}
- metrics_reported=yes: 43/83
- baseline_compared=yes: 41/83
- limitations_stated=yes: 67/83
- code_available=yes: 3/83
- data_available=yes: 16/83

## Year

- 2020: 1
- 2021: 5
- 2022: 2
- 2023: 8
- 2024: 8
- 2025: 31
- 2026: 45

2025–2026 share: **76.0%**

## Grid domain (full text n=83)

- distribution: 11
- ev_charging: 6
- microgrid: 6
- multi: 47
- substation: 1
- transmission: 5
- unclear: 7


---

## Round-3 revision additions (2026-10-19)

### Matched denominators (Flaw 3 fix)

| Subset (full text) | n | any AI-threat | substantive |
|---|---|---|---|
| all full-text | 83 | 35 (42.2%) | 11 (13.3%) |
| non-review | 49 | 20 (40.8%) | 6 (12.2%) |
| security-primary, non-review | 41 | 16 (39.0%) | 6 (14.6%) |
| security-primary, non-review, ML-detection | 29 | 16 (55.2%) | 6 (20.7%) |
| journal-only | 62 | 26 (41.9%) | 9 (14.5%) |

- ML role split: detection 55, forecasting 12, control 3, none 13. Forecasting/control are
  not security functions → security-relevant defensive ML = 55/83 (66.3%), not 70/83.
- 30/55 detection-ML studies engage an AI threat.

### Year-wise profile (full text, n=83) — descriptive only (ranked, recency-weighted corpus)

| year | n | ML | any | subst |
|---|---|---|---|---|
| 2020 | 1 | 0 | 0 | 0 |
| 2021 | 3 | 0 | 0 | 0 |
| 2022 | 2 | 2 | 1 | 1 |
| 2023 | 6 | 4 | 0 | 0 |
| 2024 | 7 | 6 | 1 | 0 |
| 2025 | 27 | 23 | 15 | 6 |
| 2026 | 37 | 35 | 18 | 4 |

### Tiered twin counts (Flaw 4 fix, full text n=83)

| Tier | Records |
|---|---|
| Twin as adversary's objective (strict target) | 1 (id 59, vehicle domain → 0 grid) |
| Names ≥1 interface threat (mitm/replay/reverse_pathway/false_command) | 44 |
| Names ≥1 model threat (poisoning/evasion/prompt) | 27 |
| Names ≥1 of either (attack channel) | 56 (overlap 15) |
| Twin as protected asset (tool) | 75 (51 also name an attack channel) |
| attack_surface_named = yes | 55 (66.3%; κ = 0.14, PABAK 0.20) |

### Strict-grid-scope sensitivity (Flaw 9 fix)

- Tier A exclusions (outside power-grid on strict reading): ids 18, 59, 69, 97 → n=79:
  ML 67, detection 52, any 33 (41.8%), substantive 10 (12.7%), strict target 0.
- Tier A+B exclusions (also 34 nuclear DT, 68 security education, 84 battery-telecom):
  n=76: ML 65, detection 50, any 32 (42.1%), substantive 10 (13.2%), strict target 0.
- Direction of the asymmetry robust to scope; magnitude moves ≤1.5 points.

### Reliability additions (Flaw 6 fix)

PABAK and bias index (max between-coder marginal difference) computed from the frozen
coder sheets; bootstrap 95% CIs (10k resamples):

| Field | %agree | κ | bootstrap 95% CI | PABAK | bias |
|---|---|---|---|---|---|
| ai_threat_overall (3-class) | 65 | 0.41 | [0.08, 0.72] | 0.48 | 0.05 |
| ai_threat_overall (any-vs-none) | 80 | 0.60 | [0.20, 0.90] | 0.60 | 0.00 |
| ai_threat_overall (subst-vs-not) | 75 | 0.14 | [−0.23, 0.64] | 0.50 | 0.05 |
| twin_role | 95 | 0.77 | [0.00, 1.00] | 0.93 | 0.05 |
| attack_surface_named | 60 | 0.14 | [−0.19, 0.49] | 0.20 | 0.30 |
| lifecycle_stage | 65 | 0.32 | [−0.07, 0.67] | 0.59 | 0.25 |

Sample frame: 20 of the 83 full-text records (24%), not 20% of 100.

### Misclassification sensitivity (Flaw 7 fix, replaces Wilson intervals)

Coder-2-as-gold-standard propagation: P(C2 engaged|C1 engaged)=7/9, P(C2 engaged|C1
zero)=2/11 → expected 35×7/9 + 48×2/11 ≈ **36 of 83 (43.3%)**, bootstrap 95% CI
**[21, 51]** (25.6%–61.4%). Coder 2 is a co-author: consistency check, not independent
validation.

### AI-wielded vs AI-attacked (construct split, substantive studies)

- AI-wielded attack generation: ids 22, 49, 57, 69
- Attacks on learned components: ids 16, 17, 24, 54, 74
- Both/mixed: ids 50, 94
- The any-engagement count (35) does not separate the two directions.

### Substantive-vector concentration

- ai_evasion=2: only id 50. ai_agentic=2: only id 50. ai_llm=2: ids 16, 50.
  → one review (id 50) supplies every substantive evasion and agentic case and half the
  substantive LLM cases.


## Round-4 additions (2026-10-19) — recomputed from the frozen coder sheets

Reproduce with `python3 analysis/reliability_round4.py`.

- **Ordinal agreement on ai_threat_overall (3x3: rows C1, cols C2 = [9,1,1],[1,3,1],[1,2,1]):**
  unweighted kappa 0.41; linear weighted kappa 0.43 (boot 95% CI 0.08-0.74);
  quadratic weighted kappa 0.44 (0.03-0.80); Gwet AC1 0.50 (0.18-0.80).
- **AC1 per field** (Table 5 AC1 column): baseline_compared 0.90, twin_role 0.94,
  ai_poisoning 0.88, threat_model_explicit 0.85, metrics_reported 0.72,
  security_primary 0.77, ml_used 0.77, ml_role 0.64, stance 0.51, dt_type 0.72,
  grid_domain 0.61, ai_adv_ml 0.59, maturity 0.41, ai_threat_overall 0.50,
  ai_evasion 0.69, eval_method 0.38, lifecycle_stage 0.54, attack_surface_named 0.31
  (lowest on both statistics), code_available 1.00, ai_agentic 0.95, ai_llm 0.89,
  data_available 0.84, stance_confidence 0.60, limitations_stated 0.60.
- **Family-level threat-vocabulary agreement (n=20):** interface family
  (mitm/replay/reverse_pathway/false_command) 17/20, kappa 0.70; classical family
  (dos/fdi/malware/physical/insider/supply_chain/hardware/other) 17/20 (85%), kappa 0.32
  (prevalence-depressed); learned-model family (poisoning/evasion/prompt) 14/20,
  kappa 0.37 (coder 2 named fewer).
- **Strict-scope sensitivity inside the 29-study core subset:** removing R18 and R69
  leaves 27 studies — 15/27 (55.6%) any, 5/27 (18.5%) substantive; removing the
  borderline records too leaves 25 — 14 any, 5 substantive.
- **Peer-review-filtered venue sensitivity:** 62 journal-classified full-text records
  minus R30, R32 (Zenodo), R65 (GSC Online Press), R69 (IRJMETS) = 58 records —
  23/58 (39.7%) any, 8/58 (13.8%) substantive, 35/58 none, 55/58 tool, 1 target
  (R59, out-of-domain).
- **ID order, verified:** IDs 1-45 are all 2026; within every year block cited_by
  descends with ID (per-record citation counts now shown in Appendix A's Cit.
  column); 40/100 records have zero citations. The IDs are a display order (year
  descending, citations descending within year) and carry no information about the
  selection rule; the clean test — year distribution of the 492 eligible records vs
  the retained 100 — needs the unreleased 492-record export, so no claim is made
  about which ranking component dominated.
- **Abstract-level twin_role for the 17 abstract-only records:** 15 tool; R91 and R92
  (Spirito et al., OSTI/INL, nuclear domain) read as attack-side work on the twin's
  interface (R91) and the twin's ML models (R92).
- **Venue/author corrections (Crossref/OSTI-verified, 2026-10-19):** R26 West Virginia
  University; R27 IEEE PARC 2026; R40 Wiley book chapter (venue_type report ->
  book_chapter; corpus profile now 3 reports / 4 book chapters); R72 ICTAACS 2025;
  R91/R92 Idaho National Laboratory / OSTI; R99 Florida International University;
  R25/R36/R75 Cyrillic author names transliterated; R75 affiliation fragments removed;
  R79 title apostrophe normalised; R32 comma-separated authors parsed.
- **24/469 (5.1%) figure:** from an unpreserved scan; relation to the ~700 probe-added
  candidates not established; treated as an unreproducible working number.
