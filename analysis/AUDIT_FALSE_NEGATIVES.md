# False-negative audit of the `ai_threat_overall` headline

**Purpose.** `ai_threat_overall = 0` for 48 of 83 full-text papers drives the headline
("57.8% engage no AI-enabled threat"). Extraction was keyword-assisted, so a threat
discussed without the coded vocabulary could be missed. This audit tests that channel
directly. **No codes changed as a result** — the 48 stand — but the audit's own power is
measured and disclosed.

## Audit 1 — strict lexicon (same vocabulary as the codebook)
Re-scanned the full text (reference lists stripped) of all 48 zero-scored papers for
attacks-on-ML phrases (adversarial example/attack, data poisoning, backdoor, model
extraction/stealing/inversion, membership inference, label flipping, prompt injection, …).

Result: **0 of 48** flagged. See `analysis/audit_false_negatives.py`.

## Positive control — is the strict lexicon even able to fire?
An audit that returns zero is only meaningful if the instrument can detect what is
known to be there. Applied the same lexicon to the **11** records coded
`ai_threat_overall = 2`.

Result: **7 of 11** fired → recall ≈ **64%**. The four misses (ids 17, 22, 57, 69) do
engage attacks-on-ML (`poisoning`/`adversarial` coded = 2) but describe them in generic
words ("stealthy", "tampering", "spoofing"), not the specific phrases. So Audit 1's "0 of 48"
cannot certify the 48 on its own — the instrument is insensitive by construction.

## Audit 2 — broad net + human adjudication
Re-scanned the 48 with a deliberately over-inclusive net: 11 families (any `adversar*`,
`poison/backdoor/trojan`, `evasion/evade`, `manipulat*` near model/data/detector,
`tamper/spoof/falsify/corrupt/compromise` near model/data/measurement, integrity attacks,
`stealthy`, `generative/GAN/deepfake`, `LLM/prompt`, `unseen/zero-day`).

- **38 of 48** fired at least one family (the net over-fires on ordinary cyberattack prose).
- **23 of 48** fired a *strong* family (`poison/backdoor`, `model-manip`,
  `model-compromise`, `evasion`).
- **All 23 were read.** Every one is a **conventional** cyberattack described in generic
  words — spoofing/falsified measurements, firmware and memory tampering, FDI,
  malware/Trojan (BlackEnergy, Havex), MITM, ARP poisoning — or a known false positive
  (Xenon-135 reactor poisoning, id 34). None presents an attack on an ML/DT model.
- Two were examined in depth and cleared: id 86 (FDIAs "bypass the current **bad data
  detection models**" — these are classical weighted-least-squares state-estimation
  residuals, not ML; the paper's LSTM is its own detector, and nothing attacks it) and
  id 15 (attacks "evade detection by the supervisor system" — a SCADA control layer;
  the paper states AI-based anomaly detection is *future* work). See
  `analysis/audit_broadscan.py`.

Result: **0 false negatives confirmed** across an over-inclusive lexicon.

## What this licenses in §7
The 48 "no engagement" records survive both a strict and a maximally broad vocabulary, and
the only genuine attacks-on-ML language in the corpus sits inside the score-2 papers
(adversarial examples, model poisoning, membership inference). Report:

1. the headline count unchanged (35/83 any; 11/83 substantive; 48/83 none);
2. the audit as a robustness check, **with its sensitivity**: the strict lexicon's recall
   on known positives is 7/11, which is *why* the broad net was run;
3. the residual, unquantifiable channel honestly — no pattern set can match wording it
   does not contain, so the audit bounds but does not eliminate the false-negative risk.

The supporting script `audit_broadscan.py` had a scope bug in its first version (the window
slicing reused a loop variable, so printed windows came from the wrong paper). Fixed; the
windows above are from the corrected run. No matrix code depended on it.
