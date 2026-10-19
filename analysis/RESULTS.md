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

