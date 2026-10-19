# Mapping: our threat vocabulary → Habeeb, Weli & Almaliki (2026) attack vectors

Habeeb, Weli & Almaliki, *Digital Twin*, 2026, DOI `10.1080/27525783.2026.2679856`, name five
attack vectors. Our codebook's closed vocabulary (`analysis/codebook.md` §4.1) was designed
independently. This table is the §4 bridge: it shows that our vocabulary **covers** all five of
their vectors and **adds** the ones their search string could not reach.

Their search string was
`("Digital Twin" OR "DT") AND ("Cybersecurity" OR "Attack Surface" OR "Defense" OR "Honeypot" OR "Intrusion Detection")`
— note the absence of any attack-side operator.

## The mapping

| # | Their vector | Our vocabulary terms | Corpus records naming it (n=83) |
|---|---|---|---|
| i | Bidirectional data-link exploitation | `mitm`, `replay`, `dos` | 26, 23, 49 |
| ii | Adversarial data poisoning on sensor streams | `poisoning`, `fdi` | 22, 46 |
| iii | AI/ML model exploitation via training-distribution attacks | `ai_adv_ml`, `ai_poisoning`, `ai_evasion` (AI-threat fields, not the threat vocabulary) | 24, 19, 9 |
| iv | Reverse attack pathway (virtual → physical actuators) | `reverse_pathway`, `false_command` | 10, 22 |
| v | Supply-chain / cross-sector | `supply_chain`, `hardware` | 19, 1 |

Every one of their five vectors is representable in our vocabulary. The mapping is a superset,
not a partition: `fdi` legitimately belongs to both (i) and (ii), which is a property of the
domain, not a defect of the codebook.

## What our vocabulary and design add

1. **`reverse_pathway` is a first-class threat term**, added specifically because their vector (iv)
   is the axis that a defence-only taxonomy cannot express. Ten records name it.
2. **`ai_llm` and `ai_agentic` as coded fields.** Their reviewed window (to Dec 2025) predates the
   LLM/agentic in grid security literature they could have found with a different search string.
   Our corpus shows 4 records engaging LLM threats and 2 engaging agentic automation, all of them
   invisible to their search.
3. **`lifecycle_stage`.** Their first named research gap is "no lifecycle-aware security
   frameworks". They name the gap; we measure it. Result: 66/83 = 79.5% of full-text records sit
   at the operation stage, and only **1** addresses design or commissioning. The gap is real and
   quantified.
4. **`twin_role`.** Their taxonomy (Sandbox, Sensor, Honeypot, Ledger) is entirely defensive. Our
   measurement: 75/83 treat the twin purely as a tool, **1/83** as a target, **0/83** as both, 7/83
   unclear. Not one paper in the corpus articulates the dual role. This is the axis their framework
   reduces to a scalar, measured at grid scale — and the measurement is that the axis has barely
   been populated.

## How to use this in the manuscript

- Place in §4 as the bridging table that lets a reader raised on their taxonomy read ours.
- Do **not** present the mapping as a critique of their search string. State it as a design
  consequence: a defence-side search cannot surface attack-side vectors, which is precisely why a
  theory-testing measurement is needed.
- The honesty constraint from `COMPETING_REVIEWS.md` still applies: they *named* AI threats in RQ1.
  Our claim is about the depth of engagement and the newer vectors, never about first mention.
