# Coding Instructions — Second Coder (C2)

**Study:** Digital Twins for Cyber-Resilient Power Grids — systematic review
**Your role:** independent second coder for the inter-rater reliability sample
**Workload:** 20 papers, approximately 10–15 hours
**Return within:** 14 days of receipt

You are one of two people coding these papers. Nobody has seen the other's answers, and that is
the entire point of the exercise — see §12.

---

## 1. Why your work matters

The review's central claim is quantitative: that grid digital-twin security research is
overwhelmingly defensive, and that almost none of it models AI as an attacker. That claim rests on
codes assigned by a human reading each paper. A reviewer will reasonably ask: *would a second
competent person, given the same rules, produce the same codes?*

If the answer is yes, the finding holds. If nobody checks, the finding is just one person's
judgement. You are the check.

Your codes are compared against the first coder's (C1) using Cohen's κ and percentage agreement.
Disagreements are not failures — they are the most useful output, because each one identifies a
rule in the codebook that is ambiguous and needs rewriting.

---

## 2. Your task, in one paragraph

Open each of the 20 PDFs listed in §5. Read enough of it to answer the coding questions — for
most papers, the abstract, introduction, methodology, evaluation and conclusion are sufficient;
skim the rest. For each paper, fill one row of `coder2_sheet.csv`, assigning a code to every blank
field according to the rules in §7–§9. Where a `2` is assigned to an AI-threat field, include a
verbatim quote with a location. Where a paper does not fit the rules, do not invent a code — leave
the field blank and write the problem in `notes` (§13).

**Do not change:** the pre-filled columns (`id` through `abstract`), the column order, or the row
order.

---

## 3. What you receive

| File | What it is |
|---|---|
| `analysis/reliability/coder2_sheet.csv` | **Your working file.** 20 rows. Columns `id`…`abstract` are pre-filled; everything after is blank and yours to fill. |
| `analysis/codebook.md` | The authoritative definition of every field. **This is your primary reference.** |
| `analysis/CODING_INSTRUCTIONS.md` | This file. |
| `papers/` | The 20 PDFs, at the paths given in the sheet's `local_path` column. |

You do **not** receive `coder1_sheet.csv`. Do not ask for it.

---

## 4. Setup

Open the sheet in a spreadsheet application, but **save it back as CSV** — not `.xlsx`. Excel and
LibreOffice will both silently mangle a CSV if you use "Save As" carelessly; use
*File → Save* (keeping the CSV format) and confirm the format prompt.

To read a PDF:

```bash
# open with your normal viewer
xdg-open papers/journals/energies/2023_irmak_digital-transformation-of-microgrids-a-review-of-design-operation-opti.pdf

# or pull the text into the terminal, which is faster for skimming
pdftotext -q <path-to-pdf> - | less
```

All paths are relative to the repository root. If a path does not resolve, tell C1 — do not
substitute a different paper.

---

## 5. The twenty papers

Each row in your sheet corresponds to one of these. Column `id` is the join key; do not renumber.

| id | Title | Venue | File |
|---|---|---|---|
| 1 | Cybersecurity and Resilience of Smart Grids: A Review of Threat Landscape, Incidents, and Emerging Solutions | Applied Sciences | `papers/journals/applied-sciences/2026_j-rgensen_cybersecurity-and-resilience-of-smart-grids-a-review-of-threat-landsca.pdf` |
| 2 | Digital twin applications and case studies in modern power grid management | Energy Reports | `papers/journals/energy-reports/2026_subramanian_digital-twin-applications-and-case-studies-in-modern-power-grid-manage.pdf` |
| 3 | Digital twins for hazard-resilient power grids: A systematic review and roadmap | Renewable and Sustainable Energy Reviews | `papers/journals/renewable-and-sustainable-energy-reviews/2026_cavus_digital-twins-for-hazard-resilient-power-grids-a-systematic-review-and.pdf` |
| 13 | Explainable digital twin–driven ensemble anomaly detection framework for cyber-physical infrastructure security | International Journal of Information Security | `papers/journals/international-journal-of-information-security/2026_erkek_explainable-digital-twin-driven-ensemble-anomaly-detection-framework-f.pdf` |
| 16 | Artificial Intelligence in Smart Grids and Power-Electronic-Interfaced Microgrids: A Systematic Literature Review of Energy Management, Optimisation, and Cybersecurity | Energies | `papers/journals/energies/2026_alsbua_artificial-intelligence-in-smart-grids-and-power-electronic-interfaced.pdf` |
| 18 | AI-Powered Cybersecurity: Graph-Based Anomaly Detection in Network Traffic | Journal of Engineering and Computational Intelligence Review | `papers/journals/journal-of-engineering-and-computational-intelligence-review/2026_zaidi_ai-powered-cybersecurity-graph-based-anomaly-detection-in-network-traf.pdf` |
| 21 | A Multi-Agent-Driven Hybrid Digital Twin Framework for Adaptive Cybersecurity Vulnerability Verification in Power Cyber-Physical Systems | Systems | `papers/journals/systems/2026_wang_a-multi-agent-driven-hybrid-digital-twin-framework-for-adaptive-cybers.pdf` |
| 22 | Using a Digital Twin for Cyber Threat Detection in Intelligent Power Grid Control Systems | Informatics and Automation | `papers/journals/informatics-and-automation/2026_kotenko_using-a-digital-twin-for-cyber-threat-detection-in-intelligent-power-g.pdf` |
| 30 | Digital Twin Technology for Real-Time Cybersecurity Monitoring in Smart Grid Infrastructure | Zenodo (CERN) | `papers/journals/zenodo-cern-european-organization-for-nuclear-research/2026_mohamed_digital-twin-technology-for-real-time-cybersecurity-monitoring-in-smar.pdf` |
| 35 | DIGITAL TWIN-BASED SMART GRID MANAGEMENT FRAMEWORK FOR SUSTAINABLE POWER INFRASTRUCTURE DEVELOPMENT IN SAUDI ARABIA | International Journal of Advanced Research | `papers/journals/international-journal-of-advanced-research/2026_khan_digital-twin-based-smart-grid-management-framework-for-sustainable-pow.pdf` |
| 43 | AI-Enabled Smart Grid: Integrating Electrical Power Systems, Computer Intelligence, and Wireless Communication Technologies | Int. J. of AI and Machine Learning | `papers/journals/international-journal-of-artificial-intelligence-and-machine-learning/2026__ai-enabled-smart-grid-integrating-electrical-power-systems-computer-in.pdf` |
| 49 | Digital Twin-Driven Intrusion Detection for Industrial SCADA: A Cyber-Physical Case Study | Sensors | `papers/journals/sensors/2025_sayghe_digital-twin-driven-intrusion-detection-for-industrial-scada-a-cyber-p.pdf` |
| 55 | Towards Intelligent Cybersecurity in SCADA and DCS Environments: Anomaly Detection Using Multimodal Deep Learning and Explainable AI | Journal of Science Research and Reviews | `papers/journals/journal-of-science-research-and-reviews/2025_oyedotun_towards-intelligent-cybersecurity-in-scada-and-dcs-environments-anomal.pdf` |
| 62 | Cybersecurity Enhancement in Digital Substations: Hidden Markov Model-Based Smart Cyber Switching and Threat Response | IEEE Access | `papers/journals/ieee-access/2025_girdhar_cybersecurity-enhancement-in-digital-substations-hidden-markov-model-b.pdf` |
| 68 | Cyber Digital Twin to improve Security Education: the RedTeam Knife approach | CHItaly | `papers/conferences/biannual-conference-of-the-italian-sigchi-chapter-chitaly/2025_barletta_cyber-digital-twin-to-improve-security-education-the-redteam-knife-app.pdf` |
| 74 | Advanced Cybersecurity Strategies for Cyber-Physical Systems: Case Studies in EV Charging Stations, Connected & Automated Vehicles, and Digital Substations | Deep Blue (Univ. of Michigan) | `papers/other/deep-blue-university-of-michigan/2025_girdhar_advanced-cybersecurity-strategies-for-cyber-physical-systems-case-stud.pdf` |
| 87 | Digital Transformation of Microgrids: A Review of Design, Operation, Optimization, and Cybersecurity | Energies | `papers/journals/energies/2023_irmak_digital-transformation-of-microgrids-a-review-of-design-operation-opti.pdf` |
| 88 | Digital Twin for Evaluating Detective Countermeasures in Smart Grid Cybersecurity | IEEE SmartGridComm | `papers/conferences/ieee-international-conference-on-communications-control-and-computing-/2023_sen_digital-twin-for-evaluating-detective-countermeasures-in-smart-grid-cy.pdf` |
| 93 | Towards electric digital twin grid: Technology and framework review | Energy and AI | `papers/journals/energy-and-ai/2022_sifat_towards-electric-digital-twin-grid-technology-and-framework-review.pdf` |
| 96 | Real-Time Digital Twin of Residential Energy Storage System for Cyber-Security Study | IEEE STPEC | `papers/conferences/ieee-international-conference-on-smart-technologies-for-power-energy-a/2021_shitole_real-time-digital-twin-of-residential-energy-storage-system-for-cyber-.pdf` |

The sample is deliberately stratified — it is not a random draw from the whole corpus. Every
stance category in the review is represented, so the reliability estimate covers all of them and
is not dominated by the most common type.

---

## 6. How to fill the sheet

1. Fill exactly the 33 columns after `abstract`. Leave `id`…`abstract` untouched.
2. One value per field, using **only** the allowed values in `analysis/codebook.md`.
3. Semicolon-separate multi-value fields (`threat_models_named`), with no space after the `;`.
4. Put `C2` in the `coder` column of every row you complete.
5. Put `no` in `adjudicated` — only C1 sets that, after we resolve disagreements.
6. Every `2` on an AI-threat field needs a verbatim quote and a location in `ai_threat_note`,
   formatted `"<quote>" (§<section or page>)`.

Fields, in sheet order:

```
stance, stance_confidence, security_primary,
dt_type, grid_domain, twin_role, attack_surface_named, lifecycle_stage,
threat_models_named, threat_count, adversary_adaptive, threat_model_explicit,
ml_used, ml_role, ml_family,
ai_threat_overall, ai_adv_ml, ai_evasion, ai_poisoning, ai_llm, ai_agentic, ai_threat_note,
eval_method, testbed_or_dataset, metrics_reported, baseline_compared,
maturity, limitations_stated, code_available, data_available,
coder, adjudicated, notes
```

---

## 7. The rules that carry the most weight

Only the four highest-stakes fields are reproduced here. **The full definitions are in
`analysis/codebook.md` and govern everything.**

### `twin_role` — the one you will be tempted to over-code
`target` = the twin is what gets attacked. `tool` = the twin is what does the defending.
`both` = the paper does both **and** discusses the tension.

A single sentence acknowledging that the twin could itself be compromised is **not** `both`. There
must be an analysis, method, threat model or experiment about it. Code `tool` and put the sentence
in `notes`.

### `adversary_adaptive`
`yes` only if the paper explicitly models an attacker who reacts to the defence — retrains,
probes, adapts. Nearly everything is `no` or `unclear`. If in doubt, `no`.

### `ai_threat_overall` (and the five sub-fields)
Ordinal 0/1/2, defined in §8. `ai_threat_overall` is **not** the maximum of the five sub-fields: a
paper can discuss AI threats generically (→ `1` overall) without addressing any specific vector
(→ `0` across all five).

### `threat_model_explicit`
`yes` only for a formal threat model with stated assumptions and attacker capabilities. **A list of
attacks is not a threat model.** Most papers are `no`, and that is itself a finding.

---

## 8. The 0 / 1 / 2 ordinal scale

Used for all six AI-threat fields.

| Code | Meaning | The test |
|---|---|---|
| **0** | Not addressed | Appears nowhere in the paper, not even in related work. |
| **1** | Mentioned or peripheral | Named in related work, listed as future work, or in one sentence. No method, no experiment, no threat model. |
| **2** | Substantive | The paper builds a method, runs an experiment, defines a threat model, or evaluates against it. |

The single most common error is coding a throwaway sentence as `2`. If the paper does not *do*
something with the concept, it is `1` at most.

---

## 9. Worked example — paper 88, coded in full

This is a real row from your sample, coded field by field, so you can calibrate before you start.

**Paper:** Sen, Bleser & Ulbig (2023), *Digital Twin for Evaluating Detective Countermeasures in
Smart Grid Cybersecurity*, IEEE SmartGridComm.
**What it does:** builds a co-simulation digital twin replicating a smart-grid cyber-physical
laboratory, reproduces attacks in both, and compares three Intrusion Detection Systems' detection
quality across the two.

| Field | Code | Reasoning |
|---|---|---|
| `stance` | `bridge` | The authors reproduce the attacks **and** evaluate defences in an explicit co-simulation testbed coupling attacker and defender. |
| `stance_confidence` | `high` | Unambiguous from abstract and methodology. |
| `security_primary` | `yes` | Evaluating detective countermeasures is the contribution. |
| `dt_type` | `system` | The twin spans process, communication and operational layers of the grid. |
| `grid_domain` | `distribution` | "the integration of digital technologies … within distribution grids". |
| `twin_role` | `tool` | The twin is the instrument for evaluating IDSs. See the boundary call in §10.1. |
| `attack_surface_named` | `yes` | Telnet, SSH, NMAP scans, IEC 60870-5-104, MTU/RTU communications. |
| `lifecycle_stage` | `operation` | The twin evaluates IDSs against a running grid's operational traffic. |
| `threat_models_named` | `dos; mitm; other` | DoS and code manipulation (§III); MITM intercepting MTU communications (§III); "Recon attack" testing NMAP-scan and failed-Telnet detection (§IV). |
| `threat_count` | `3` | Three distinct vocabulary entries. |
| `adversary_adaptive` | `no` | No adaptive attacker; scenarios are fixed and replayed. |
| `threat_model_explicit` | `no` | Attacks are enumerated as scenarios. No assumptions/capabilities/knowledge model. |
| `ml_used` | `no` | The three IDSs are signature-based, specification-based and statistical-anomaly-based. ML appears only as future work. |
| `ml_role` | `none` | |
| `ml_family` | *(empty)* | |
| `ai_threat_overall` | `0` | No AI-enabled threat is discussed anywhere. |
| `ai_adv_ml` | `0` | |
| `ai_evasion` | `0` | |
| `ai_poisoning` | `0` | |
| `ai_llm` | `0` | |
| `ai_agentic` | `0` | |
| `ai_threat_note` | *(empty)* | Nothing reached `2`, so no quote is required. |
| `eval_method` | `mixed` | Co-simulation plus hardware-in-the-loop, cross-checked against a physical laboratory. |
| `testbed_or_dataset` | `modular co-simulation framework (power-grid simulation + communication-network emulation, Purdue-model SCADA lab); IDSs: Snort, specification-based, statistical anomaly-based` | |
| `metrics_reported` | `yes` | Detection quality compared across DT and laboratory. |
| `baseline_compared` | `yes` | Three IDSs compared against each other and against the physical laboratory. |
| `maturity` | `validated` | Evaluated against a physical reference system, not only the authors' own scenario. |
| `limitations_stated` | `yes` | Conclusion names fidelity, real-time simulation and adaptation to evolving grid dynamics as challenges. |
| `code_available` | `no` | Nothing released. |
| `data_available` | `no` | Nothing released. |
| `coder` | `C2` | |
| `adjudicated` | `no` | |
| `notes` | `Twin-as-target acknowledged in one sentence: "the security of the twin itself is crucial, as its compromise could provide misleading results or expose real system vulnerabilities." Not treated, so twin_role=tool. ML-based IDS is future work only — not coded as AI-threat engagement.` | |

Note what this example demonstrates: the paper is security-focused and sophisticated, and still
scores **0 on every AI-threat field**. That is expected and is the pattern the review is measuring.
Do not go looking for AI threats that are not there — a genuine `0` is a finding, not a miss.

---

## 10. Boundary calls

Three constructed cases for the decisions that cause the most disagreement. These are teaching
examples, not corpus papers.

### 10.1 `twin_role`: `tool` vs `both`
> A paper builds a twin to test a detector. In the conclusion: *"one limitation is that the twin
> itself could be attacked, which we leave to future work."*

**Code `tool`.** Recorded in `notes` as an acknowledgement. `both` requires the paper to actually
analyse, model or test the twin's own compromise. A one-sentence caveat is not treatment — and the
frequency of exactly this sentence, without follow-through, is one of the review's findings.

### 10.2 `ai_threat_overall`: `0` vs `1` vs `2`
> **(a)** The introduction says *"AI-based detectors are themselves vulnerable to adversarial
> examples [12]."* Nothing further.
> **(b)** The paper trains a detector, generates adversarial examples against it, and reports the
> detection-rate drop.
> **(c)** The paper generates adversarial examples and evaluates an adversarial-training defence.

**(a) = 1** — acknowledged, cited, not studied. **(b) = 2**, `ai_adv_ml = 2`. **(c) = 2**,
`ai_adv_ml = 2` — a defence *against* an AI threat still counts as engaging it. Coding (c) as `0`
because the paper is "defensive" is the single most damaging error you could make in this study.

### 10.3 `stance`: `defensive` vs `bridge`
> Two papers both report a 95% detection rate.

One uses the **public dataset's** fixed attack set → `defensive`.
One **generates its own attack scenarios**, then evaluates the detector → `bridge`.

The test is not how good the results are. It is whether the authors built the threat.

---

## 11. Pace

Roughly 10–15 hours total, i.e. 1–2 papers per day over two weeks. Papers 1, 3, 16 and 87 are
reviews and are fast. Papers 13, 21, 49 and 62 are method-heavy and take longest. Paper 74 is a
dissertation — read the abstract, introduction and conclusions only; do not read it end to end.

Do not rush the last five papers. Accuracy across all 20 matters more than finishing early; a
half-coded paper is worse than a late one.

---

## 12. Independence rules

These are not formalities — they are what make the statistic meaningful.

1. **Do not discuss any paper with C1** until you have submitted your sheet.
2. **Do not look at `coder1_sheet.csv`,** the OpenAlex screening labels, or any other file that
   reveals a classification.
3. **Do not consult the paper's own keywords or author-assigned categories** for `stance` — the
   decision must come from your reading against the codebook.
4. If you recognise a paper and already know how it was categorised elsewhere, say so in `notes`
   for that row.
5. If you find a codebook rule ambiguous, write your best call **and** flag it in `notes`. Do not
   pause to ask mid-stream unless the paper is genuinely uncodable.

---

## 13. Escalation

If a paper does not fit the rules: leave the disputed field **blank**, put the problem in `notes`,
and carry on. Blank fields are visible and get adjudicated. A guessed field is invisible and
corrupts the dataset.

At the end, send C1 a short summary listing the rows you escalated and what the problem was. Every
escalation becomes a codebook revision.

---

## 14. What happens to your coding

1. C1's and your sheets are compared field by field on the 20 shared rows.
2. Agreement is computed per field: **Cohen's κ** for multi-class fields (target κ ≥ 0.61) and
   **percentage agreement** for the sparse AI-threat fields.
3. Some AI-threat fields will have κ = `nan`. This is expected, not a bug: κ is undefined when a
   category has zero variance, and if both coders agree the corpus contains zero attempts at
   adversarial ML, the statistic cannot be computed. We report percentage agreement and state why.
4. Every disagreement is reviewed and adjudicated against the codebook. The adjudicated value is
   what enters the analysis.
5. Ambiguous rules are rewritten. If we disagree systematically on one field, the codebook was
   wrong, not you.

You will be acknowledged in the paper's acknowledgements section, and you may be offered
co-authorship if your contribution extends beyond coding. Say now if you do **not** want to be
named.

---

## 15. Deliverable

Return by the agreed 14-day deadline:

- `coder2_sheet.csv` — 20 rows, all 33 coding columns filled, same column and row order you
  received, saved as CSV.
- A short escalation note (plain text or in `notes`) listing any row you could not code and why.
- A one-line answer to: **"was any codebook rule ambiguous enough to change a decision?"** — and if
  yes, which.

---

## 16. Confidentiality

The corpus, the matrix and the other coder's sheet are unpublished research materials. Do not
share, redistribute or reuse them outside this project. The 83 PDFs are copyrighted and were
obtained for research use; do not re-upload them anywhere.

---

## Questions

Ask C1 about anything procedural (files, paths, formats, deadlines). Ask nothing about how a
specific paper should be coded — that is the thing being measured, and the answer would invalidate
the exercise. Codebook ambiguities go in `notes`, not in a message.
