# Codebook — Digital Twin Grid Cybersecurity Systematic Review

Version 1.0 · 2026-10-16

This is the **authoritative** definition of every field in `extraction_matrix.csv`.
If this file and the matrix ever disagree, this file wins and the matrix is wrong.

Two coders apply these rules. Any rule that is ambiguous gets escalated and added here as a
worked example rather than decided case-by-case — otherwise the reliability statistic is
meaningless.

---

## 0. Ground rules

1. **Code what the paper says, not what you know.** If the paper does not state something, code
   `unclear` or `no`. Never infer from the abstract what the full text does not support.
2. **Denominators.** Fields marked `[FT]` are full-text-coded and exist only for the 83 records
   with a PDF. Fields marked `[ABS]` are coded from title + abstract for all 100.
3. **Evidence.** Any code of `2` on the AI-threat fields must carry a verbatim quote in
   `ai_threat_note`, plus a page or section reference. A `2` without a quote is invalid.
4. **Independence.** Coders do not see each other's sheets until both are submitted.
5. **Uncertainty is a valid answer.** `unclear` is a real code. Guessing corrupts the study.

### The 0 / 1 / 2 ordinal scale (used for all AI-threat fields)

| Code | Meaning | Test |
|---|---|---|
| **0** | Not addressed | The concept appears nowhere in the paper, not even in related work. |
| **1** | Mentioned or peripheral | Named in related work, listed in future work, or acknowledged in one sentence. No method, no experiment, no threat model built around it. |
| **2** | Substantive | The paper builds a method, runs an experiment, defines a threat model, or evaluates against it. One sentence is never enough. |

Worked boundary: a paper that says *"future work should consider adversarial examples"* is **1**.
A paper that generates adversarial examples against its own detector and reports the resulting
detection drop is **2**.

---

## 1. Identifiers and bibliographic fields (pre-filled, do not edit)

| Column | Type | Notes |
|---|---|---|
| `id` | int 1–100 | Stable corpus index. Never renumber. |
| `title` | text | Pre-filled. |
| `authors` | text | Pre-filled, `;`-separated. |
| `year` | int | Pre-filled. |
| `venue` | text | Pre-filled, normalised venue name. |
| `venue_type` | enum | `journal` \| `conference` \| `book_chapter` \| `thesis` \| `report` \| `preprint`. Pre-filled. |
| `publisher` | text | Pre-filled. |
| `doi` | text | Pre-filled; empty for 3 repository records. |
| `doi_status` | enum | Pre-filled. `verified` \| `no_doi` \| `non_resolving` \| `unverified`. |
| `cited_by` | int | Pre-filled from OpenAlex. Snapshot value, do not update. |
| `fulltext` | enum | Pre-filled. `yes` (83 records) \| `no` (17 records). |
| `local_path` | text | Pre-filled path to the PDF, empty when `fulltext = no`. |

---

## 2. Abstract-level fields

Coded from title + abstract. Done for **all 100** records.

### 2.1 `stance` `[ABS]`

What is the paper's relationship to the security problem? Assign exactly one.

| Value | Decision rule | Typical signal |
|---|---|---|
| `adversarial` | The paper *attacks* a grid or twin system, or studies how it can be broken. | Builds an attack, demonstrates exploitation, analyses an attack chain. |
| `defensive` | The paper *protects* — detects, prevents, mitigates, or recovers. | Proposes a detector, validates a framework, hardens a protocol. |
| `bridge` | Genuinely does both, with a real attack **and** a real defence, or an explicit co-simulation testbed coupling attacker and defender. | "We generate FDI attacks and then evaluate our detector against them." |
| `review` | Primary purpose is to survey, map or synthesise existing work. | Systematic review, survey, taxonomy, bibliometric study. |
| `enabling` | Advances the digital twin itself (architecture, modelling, data, performance) with security only secondary or absent. | Twin framework for monitoring; security mentioned as motivation only. |

**Disambiguation rules**

- Attack + defence both present → `bridge`, *not* `defensive`. `defensive` is for papers where the
  attack exists only as a fixed test set.
- A survey that also proposes a framework is still `review` — its primary purpose is synthesis.
- Security is the *motivation* but not the *contribution* → `enabling`.
- Tie between `defensive` and `bridge`: ask whether the paper's own author built the attack. If no,
  it is `defensive`.
- `review` vs `enabling` for a *survey of DT applications*: if the paper surveyed prior work
  (a literature/database method), it is `review`, even when security is a minor section. Reserve
  `enabling` for a paper that proposes or advances a DT artefact. **[revision R2]**
- `defensive` vs `bridge` when the authors *generate* attack data or *inject* attacks into their
  own twin: that is `bridge`, even if the attacks exist only to test a detector. **[revision R2]**

### 2.2 `stance_confidence` `[ABS]`

`high` \| `medium` \| `low`. Code `low` whenever the abstract alone genuinely cannot decide it —
these are the cases that get escalated to adjudication.

### 2.3 `security_primary` `[ABS]`

`yes` \| `no`. Is cybersecurity a primary contribution, or only a motivation/backdrop?
This differs from `stance`: an `enabling` paper can still have `security_primary = no`.

---

## 3. Classification fields `[FT]`

### 3.1 `dt_type`

`asset` (one component, e.g. a transformer) \| `process` (a control or operational process) \|
`system` (a network, feeder, or whole-grid twin) \| `mixed` \| `unclear`.

### 3.2 `grid_domain`

Assign one **primary** domain; note secondaries in `notes`.
`transmission` \| `distribution` \| `microgrid` \| `der` \| `ev_charging` \| `substation` \|
`market` \| `multi` \| `unclear`.

### 3.3 `twin_role` — **critical field**

Where does the digital twin sit relative to the threat?

| Value | Meaning | Test |
|---|---|---|
| `target` | The twin is what gets attacked. | The paper attacks the twin's interface, data feed, or model. |
| `tool` | The twin is what does the defending. | The twin is used to detect, simulate safely, or rehearse attacks. |
| `both` | The paper explicitly does both and discusses the tension. | Rare — expect very few. Report every instance in `notes`. |
| `unclear` | Not stated. | |

This field carries the paper's central argument. Code it conservatively and note the evidence.

### 3.4 `attack_surface_named`

`yes` \| `no`. Does the paper name the concrete surface being attacked (an API, a data
acquisition link, a model input, a comms protocol), as opposed to discussing attacks in the abstract?

Code `yes` only when a **specific interface, protocol, or device input** is named (e.g. "the
Modbus/TCP link to the PLC", "the PMU measurement input", "the GOOSE message bus"). Naming an
attack *type* ("FDI", "DoS") or an asset class ("the IED") is **not** naming a surface. **[revision R3]**

### 3.5 `lifecycle_stage`

Which stage of the digital twin's lifecycle is protected, or where does the security mechanism sit?

`design` \| `commissioning` \| `operation` \| `maintenance` \| `decommissioning` \| `multi` \| `unclear`.

Assign one primary stage; use `multi` only when the paper explicitly addresses more than one. This
field exists to test a live gap claim — the 2026 Dual-Role review names "absence of lifecycle-aware
security frameworks" as its first research gap, without measuring lifecycle coverage itself.
Code from the paper's own framing, not from where a deployment would conventionally sit.

Mentioning a second stage in passing (e.g. "maintenance" inside a limitations sentence) does **not**
trigger `multi`; the paper must frame its security contribution across more than one stage. A
single-stage paper that merely lists the lifecycle in a figure is `operation`. **[revision R4]**

---

## 4. Threat model `[FT]`

### 4.1 `threat_models_named`

Semicolon-separated, drawn **only** from this closed vocabulary:

```
fdi             False Data Injection
replay          Replay / record-and-replay
dos             DoS / DDoS
mitm            Man-in-the-middle
false_command   Malicious/false command injection
supply_chain    Supply-chain compromise
hardware        Hardware trojan / physical implant
physical        Physical/kinetic attack on equipment
insider         Insider threat
malware         Malware / ransomware
poisoning       Data or model poisoning
evasion         Evasion of an ML detector
prompt          Prompt injection / LLM manipulation
reverse_pathway Compromised virtual/twin model propagates erroneous commands
                back to physical actuators (Habeeb et al. 2026, vector iv)
other           Anything else — define it in `notes`
```

Empty string if the paper names no threat model.

### 4.2 `threat_count`

Integer = number of distinct vocabulary entries in `threat_models_named`.

### 4.3 `adversary_adaptive`

`yes` \| `no` \| `unclear`. Does the paper assume an adversary who **reacts to the defence** —
retrains, adapts, probes the detector? The overwhelming default in the literature is `no`; code
`yes` only when the paper explicitly models an adaptive or moving adversary.

### 4.4 `threat_model_explicit`

`yes` \| `no`. Is there a formal threat model (assumptions, capabilities, knowledge), or are
attacks simply enumerated in a list?

---

## 5. AI/ML fields `[FT]`

| Column | Values | Notes |
|---|---|---|
| `ml_used` | `yes` \| `no` \| `unclear` | Does the paper use ML/AI at all? |
| `ml_role` | `detection` \| `control` \| `forecasting` \| `co_simulation` \| `none` \| `other` | Primary role. |
| `ml_family` | controlled vocabulary, `;`-separated | CNN, LSTM, GRU, RNN, GNN, transformer, PINN, RL, SVM, RF, XGBoost, kNN, DNN, NN, autoencoder, ensemble, federated, GAN, HMM, LOF, elliptic-envelope, ML, DL, other. No prose. **[revision R5]** |

---

## 6. AI-threat engagement — the headline fields `[FT]`

Six fields, each on the 0/1/2 scale from §0. Together they produce the paper's central number.

| Column | Question it answers |
|---|---|
| `ai_threat_overall` | Does the paper engage *any* AI-enabled threat against the twin or its ML, at all? |
| `ai_adv_ml` | Adversarial ML / adversarial examples against a grid detector or twin model |
| `ai_evasion` | Evasion of an ML detector — inputs crafted to slip past it |
| `ai_poisoning` | Training-data or model poisoning, backdoors |
| `ai_llm` | LLM-specific threats — prompt injection, model extraction, jailbreak |
| `ai_agentic` | Autonomous or agentic attack automation |

**Rules**

1. `ai_threat_overall` is **not** the maximum of the other five. A paper can discuss AI threats
   generically without addressing a specific vector — that is `1` overall and `0` throughout.
2. Code `1`, not `0`, when the concept is acknowledged but not studied. The distance between
   "absent" and "acknowledged" is itself a finding.
3. Every `2` needs a verbatim quote + location in `ai_threat_note`.

### 6.1 `ai_threat_note`

Free text. Format: `"<verbatim quote>" (§<section/p.>)`. Required for any `2`; optional but
encouraged elsewhere.

---

## 7. Evaluation and rigour `[FT]`

| Column | Values | Definition |
|---|---|---|
| `eval_method` | `simulation` \| `testbed` \| `hil` \| `field` \| `qualitative` \| `conceptual` \| `mixed` | How the claim was tested. `conceptual` = no evaluation at all. Precedence: a hardware-in-the-loop rig → `hil`; a named laboratory/bench or synthetic-but-instantiated rig → `testbed`; a bare simulator or public dataset → `simulation`; no experiment (argument/architecture only) → `qualitative` or `conceptual`; only genuinely heterogeneous evidence across several of these → `mixed`. **[revision R6]** |
| `testbed_or_dataset` | free text | Named testbed, simulator (e.g. RTDS, OPAL-RT, GridLAB-D, IEEE 13-node) or dataset. Empty if none. |
| `metrics_reported` | `yes` \| `no` | Are quantitative metrics given? |
| `baseline_compared` | `yes` \| `no` | Is the method compared against an alternative or a baseline? |
| `maturity` | `concept` \| `prototype` \| `validated` \| `deployed` | `validated` = evaluated against something beyond the authors' own scenario. A survey, review, or thesis with no new artefact is `concept`; a new artefact tested only in the authors' own scenario is `prototype`. **[revision R6]** |
| `limitations_stated` | `yes` \| `no` | Does the paper state its own limitations? |
| `code_available` | `yes` \| `no` \| `partial` | Is code released? |
| `data_available` | `yes` \| `no` \| `partial` | Is data released? |

---

## 8. Coder bookkeeping

| Column | Values | Notes |
|---|---|---|
| `coder` | `C1` \| `C2` | Who filled this row. |
| `adjudicated` | `yes` \| `no` | Set to `yes` only after a documented resolution of a disagreement. |
| `notes` | free text | Anything this codebook could not accommodate. Every entry here is a candidate codebook revision. |

---

## 9. Escalation

If a paper does not fit these rules, do **not** invent a value. Put the row's `coder` value in,
leave the field empty, and write the problem in `notes`. Report these in the weekly check-in so
they become codebook revisions rather than silent inconsistencies.

---

## 10. Adjudication (added after the reliability round)

The 20-paper double-coding produced 149 field-level disagreements. They were resolved against
this codebook, not case by case:

1. **Deciding rule.** Adopt the value the codebook + evidence dictate. Where the codebook was
   ambiguous, fix the *rule* above (revisions R2–R6) and then apply it.
2. **Tie-break.** Where both values are defensible and the evidence cannot separate them, **C1
   prevails** (the primary full-text coder) and the ambiguity is logged here. This is stated in the
   paper's methods; it is not a hidden thumb on the scale.
3. **Where an adjudicated value is neither coder's**, the codebook rule decides. Two cases:
   ids 55 and 62 → `eval_method = hil` (both coders missed the HIL rig; R6).
4. **Resolution is written to** `codes/adjudicated.txt` (non-empty fields override C1). `merge_codes.py`
   applies it to `extraction_matrix.csv` and sets `adjudicated = yes`. `coder1_codes.csv` is frozen
   before the overlay so the reliability statistic still compares C1's primary coding against C2.

### Revision log

| Rev | Date | Change |
|---|---|---|
| R2 | 2026-10-16 | `stance`: review-vs-enabling rule for DT-application surveys; attack-generating papers are `bridge`, not `defensive`. |
| R3 | 2026-10-16 | `attack_surface_named`: `yes` requires a named interface/protocol, not an attack type. |
| R4 | 2026-10-16 | `lifecycle_stage`: passing mentions do not trigger `multi`. |
| R5 | 2026-10-16 | `ml_family`: free text contracted to a controlled vocabulary. |
| R6 | 2026-10-16 | `eval_method`: explicit precedence (hil > testbed > simulation); `maturity`: surveys/hypothesis-only work is `concept`. |
