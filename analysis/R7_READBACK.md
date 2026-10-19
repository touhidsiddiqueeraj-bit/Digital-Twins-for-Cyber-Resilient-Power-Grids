# Round-7 readback: the three "feasible now" inspections, done

This file documents three inspections that earlier revisions of the manuscript stated as
required future work, and that a reviewer correctly noted are feasible now. All three were
conducted on 2026-10-19 by a single author of the review, post hoc, with the coded values
known to the reader. They are **not** independent re-coding: they are author readbacks of
released artifacts (stored abstracts + the released full-text keyword windows in
`analysis/evidence/broadscan.txt`) and, for R91, the report's full text. No value in
`extraction_matrix.csv` was changed; the frozen adjudicated matrix is untouched.

## 1. Inspection of the 15 weak audit firings

The broad-net audit of the 48 records coded `ai_threat_overall = 0` fired at least one
family on 38 records: 23 strong firings (individually inspected at audit time) and
**15 weak-only firings** (ids 3, 7, 10, 11, 13, 18, 21, 25, 39, 45, 63, 77, 80, 88, 100)
that were previously reported as uninspected. All 15 were now read, window by window,
from the released `broadscan.txt` output, with the stored abstract alongside.

**Result: no substantive (score-2) false negative; at most two score-1 (any-level)
borderline cases.**

- **13 of 15 cleared.** The firings are: acronym lists (R19-style `RUL-GAN`/`GAN` in
  abbreviation tables), classical adversary prose (APT groups, MITM, FDI, Stuxnet,
  BlackEnergy/Havex: R7, R13, R63, R80, R93 and others), defensive capability claims
  ("detects previously unseen attacks": R13, R18), related-work AI mentions (GAN-based
  IDS in others' work: R11, R19), twin-synthesised training data (R25), and one
  future-work plan (R11: "we plan to ... employ GANs to synthesize sophisticated attack
  data" — a plan, not a treatment, so score 0 stands under the codebook).
- **R21 (borderline).** Red-team/blue-team multi-agent attack simulation with an
  adversarial RL curriculum ("the red team must search for alternative paths or stealthier
  actions"). Under a broad reading of agentic attack automation this is a score-1
  engagement; under the codebook's requirement that the record engage the threat itself
  (rather than use agents as a defensive training mechanism) the 0 stands. Flagged, not
  re-scored.
- **R100 (borderline).** The final sentence of the body states that attackers can use
  deep learning "to enhance the speed, accuracy and predictability of the attacks." If
  read as an acknowledged AI-wielded attack vector this is a one-sentence (score-1)
  mention; the 0 coding is defensible because the sentence is unsupported and
  undeveloped, but this is the single most plausible any-level miss of the 15. Flagged,
  not re-scored.
- **R88 (noted for the twin-position analysis, not for AI threats).** One window states
  that "if an adversary compromises the DT, it could lead to unauthorized data access,
  manipulated simulations, security vulnerabilities in the real-world system, intellectual
  property theft" — a generic twin-as-compromise-object sentence with no AI component and
  no development. R48 (found in the sample re-read below) contains a similar one-liner
  ("[the DT grid] ... is a main target for hackers"). Neither moves any AI-threat code;
  both show that the corpus contains undeveloped twin-as-object language that the strict
  `twin_role` rule deliberately does not count.

If both borderline records were re-scored to 1, any-level engagement would move from
35/83 (42.2%) to 37/83 (44.6%); the substantive count is unchanged by the inspection.

## 2. Seeded sample re-read of the negatives

A seeded uniform sample (seed 7) of 12 of the 48 zero-coded records was drawn:
R9, R10, R13, R19, R48, R62, R65, R79, R81, R85, R89, R93. For each, the stored
abstract (title + abstract as held in the papers CSV) and every released broad-scan
window were read and the any-engagement judgement re-made.

**Result: 12 of 12 confirmed at 0 on the assembled evidence.**

Typical clearance patterns: GAN hits that are acronym lists (R19); "model-compromise"
hits that are classical FDI/MITM/DoS on measurements and SCADA (R62, R65, R79, R81, R85);
Stuxnet/BlackEnergy incident history (R48, R93); synthetic-data generation by the twin
itself (R9, R25); defensive detection claims only. R79 and R89 fired no family at all in
the full-text scan. The one substantive-adjacent finding is the R48 twin-as-target
one-liner quoted above. The re-read is abstract-plus-window level, not a full-text
re-read; an independent (non-author) full-text re-read with a miss-rate estimate remains
the design that would bound the false-negative channel.

## 3. R91 and R92 read: the twin-as-target counterexamples, in the corpus's own records

Both abstract-only records were obtained and read on 2026-10-19:

- **R91** (Spirito, Ly & Veretennikov 2023, INL/RPT-23-75113, DOI 10.2172/2337610):
  full text (48 pp.) obtained from the INL digital library
  (`inldigitallibrary.inl.gov/sites/sti/sti/Sort_74726.pdf`; the OSTI purl endpoint was
  unreachable from this environment).
- **R92** (Spirito, Zhang & Hossain 2023, INL/RPT-23-75114, DOI 10.2172/2331253):
  the report's own extended abstract was obtained from the OSTI record; the full-text
  PDF could not be retrieved from this environment (two attempts, documented in
  `SEARCH_PROVENANCE.md`).

**What R91 contains.** An attack-surface analysis of the digital twin and its advanced
sensor/instrumentation interfaces in advanced reactor architectures. Attacks are
classified by intended target across the twin's physical, digital and communication
sections, with scenario demonstrations: a server-side request forgery exploit of a cloud
(Azure) digital-twin instance used to exfiltrate the twin, replicate it offline in
simulation mode, and dry-run attacks; data deception of the twin's autonomous control
("by modifying the data received by the digital twin, it was deceived into throttling the
output from the power supplies" — the scenario outcome is reactor damage); private-5G
jamming that starves the twin of real-time data; and sensor supply-chain compromise
(counterfeit sensors). Countermeasures occupy the second half (cyber-informed
engineering; secondary sensors with trust-weighted consensus and self-triggered
control). The twin's ML/AI components are named as attack-relevant dependencies
("the digital twin ML and AI models are used to collect and calibrate sensor readings").
The attack mechanisms are classical (SSRF, jamming, data manipulation); the AI-specific
vectors are not the mechanism.

**What R92 contains.** Construction of a "multi-rate time-changing intelligent
coordinated hyperparameter attack" against the digital twin's machine-learning models —
hyperparameters are repeatedly altered "using both random and intelligent optimal
techniques", at varied rates and in varied amounts, "to improve stealth and flexibility" —
together with an event-triggered predictive-control response (sliding-window linear
regression; Lyapunov-Krasovskii-derived control gain), demonstrated in simulation. The
attack object is the twin's ML models themselves.

**Post-hoc author coding (single-coder, not blind, not merged into the matrix):**

| Record | Domain | twin_role reads as | ai_threat_overall reads as | Basis |
|--------|--------|--------------------|-----------------------------|-------|
| R91 | nuclear | both (twin attacked as object and pathway; also protected) | 1 (ML named as compromised dependency; mechanisms classical) | full text |
| R92 | nuclear | both (twin's ML models are the attack object; response strategy defends) | 2 (dedicated attack construction + defence + simulation) | extended abstract |

**What this changes.**

1. The unqualified statement "no study treats the twin as the adversary's objective" is
   contradicted by read evidence inside the retained 100. The defensible statement is
   domain-scoped: **no grid-domain study** in the corpus does so; the corpus's own
   nuclear-domain records do, and at least one (R92) attacks the twin's ML models
   directly.
2. `both = 0` among the 83 full-text records is a statement about the coded frame, not
   an impossibility result: both post-hoc reads return `both`, so the category is
   attainable in adjacent domains.
3. P1 is reframed from "nobody attacks twins" to a grid-domain gap with named
   nuclear-domain counterexamples and an explicit transferability question (see the
   revised agenda).
4. Neither record changes any count over the 83 full-text records; both remain outside
   the strict grid scope; the full-text matrix remains frozen exactly as released.
