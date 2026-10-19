# Response to the round-3 review

**Decision addressed:** "Reject in its current form. Major restructuring required before
resubmission."

**What was done.** The manuscript was restructured around the reviewer's nine fatal flaws
and the presentation list. Every change below is in this branch; the rebuilt
`manuscript.pdf` (56 pp.) compiles cleanly. Where a demanded fix required data that do not
exist in the released package, the demand is met *by declaring the limit and specifying the
artifact that would resolve it*, not by asserting a defence the data cannot support.

The reviewer's summary of what the paper shows is accepted as the correct reading, and the
abstract now says it in those terms: in the top 100 ranked records of one database, coded
mostly by one author from keyword-assisted reading, short mentions of AI threats appear in
about half of the ML-using studies; the paper's contribution is the quantified asymmetry of
emphasis *within a declared corpus*, not a claim about the literature.

---

## Fatal flaw 1 — ranked sample manufactures the result

**Required:** code all 492 eligible records, or a random sample; otherwise drop
"systematic" from the title.

**Done: dropped "systematic".**

- Title is now *"Digital Twins for Cyber-Resilient Power Grids: A Structured Corpus Review
  of Defensive and Attack-Side AI, with a Research Agenda."* Keyword updated.
- §4.1 now states plainly: not a systematic review in the PRISMA sense — one database, no
  registered protocol, a ranked non-random subset; PRISMA *flow format* is used only so the
  selection rule is exposed, not hidden.
- The top-100 cut is relabelled **Selection (non-probabilistic)** in Figure 1 and in the
  text, and its direction biases are stated: favours reviews (36% of corpus) and cited
  defensive work, penalises new uncited attack-side work.
- The 76% 2025–26 figure is marked as a selection artefact in the body text (not just the
  caption), in the abstract, and in the conclusion.
- Coding the 492 is not possible from the released package (the 492-record export is not
  in the repository), so it is specified as the upgrade path in `SEARCH_PROVENANCE.md`
  rather than claimed as done.

## Fatal flaw 2 — probes cannot be shown to have influenced the corpus

**Required:** rebuild per-record provenance; report probe-only share of the 100 and the
492; rerun the headline on that subset.

**Done: the void defence is withdrawn; the gap is declared and specified.**

- §4.2 (Search) now states that the screened 1,287 derive from the twelve core queries,
  that per-record query provenance for the ~700 probe-added records was not retained, and
  that the retrieval-bias defence the probes were designed to provide *cannot be made from
  these data* — "and we do not make it."
- The §6.5 argument ("ours adds four adversarial-AI probes and still finds shallow
  engagement, so the gap is not merely their query's doing") is **removed** and replaced
  with the opposite statement: the asymmetry may be overstated in the un-retrieved
  attack-side literature.
- §8.5 (Search bias) explicitly withdraws the earlier robustness claim and states that,
  on the released evidence, the corpus derives from the core vocabulary alone.
- Figure 1 now shows the probes as a separate annotation ("screening status not
  established in released record") instead of the old "2,000 incl. probes" line that
  implied they were screened.
- New file **`SEARCH_PROVENANCE.md`** inventories what is released, declares the gap, and
  lists the five artifacts whose release resolves it (query strings, run dates, per-record
  provenance, full pool export, headline re-run on the probe-only subset).
- The literal rebuild could not be executed in this revision: the original query strings
  are not in the repository, so re-execution would not reproduce the original pool (an
  OpenAlex re-run attempt was also blocked by API rate limits at revision time). This is
  disclosed rather than papered over.

## Fatal flaw 3 — "defensive AI" inflated; mismatched denominators; no rate test

**Required:** report engagement within security-primary, non-review, detection-ML studies;
add a year-wise analysis or retract "faster."

**Done: all three.**

- The abstract and §5.5 now separate ML use (70/83) from its security-relevant role:
  **detection 55/83 (66%)**; forecasting (12) and control (3) are named as not security
  functions. "AI is used defensively in 70 of 83" no longer appears.
- The denominator the reviewer asked for is computed and reported: **security-primary,
  non-review, ML-detection, n = 29 → 16 (55%) any engagement, 6 (21%) substantive**;
  intermediate tiers (non-review 20/49; security-primary non-review 16/41) are also
  reported, and all subsets are in the expanded denominator table (Table 2).
- "Far faster"/"adopts faster" is **retracted** everywhere (abstract, intro, §6.1,
  conclusion). The claim is now an asymmetry of *emphasis*, explicitly not a rate claim.
- New Table (`tab:yearwise`): year-wise ML use vs any/substantive engagement for all seven
  corpus years, labelled descriptive-only because the corpus is recency-weighted. No
  temporal conclusion is drawn from it.
- The "two-sentence mention counts as engagement" point is met by the existing 0/1/2
  scale reporting (mentioned vs substantive) and by the new concentration disclosure (see
  presentation items): all substantive evasion and agentic cases, and half the substantive
  LLM cases, sit in one review.

## Fatal flaw 4 — "twin as target = 1" is definitional; looser count uncomputed

**Required:** compute the looser count; report target / attack-surface / asset together
with `attack_surface_named` prevalence; remove the vehicle record under grid scope.

**Done: computed, reported as tiers, vehicle record excluded from grid claims.**

- New Table (`tab:twintiers`) and §5.3 rewrite report the tiers side by side: strict
  target **1** (of which grid-domain **0**); names ≥1 interface threat
  (mitm/replay/reverse-pathway/false-command) **44**; ≥1 model threat
  (poisoning/evasion/prompt) **27**; either (attack channel) **56** (overlap 15); twin as
  protected asset **75**, **51** of which also name an attack channel;
  `attack_surface_named` = **55/83 (66.3%)** with its κ = 0.14 / PABAK 0.20 attached.
- The reviewer's argument is adopted verbatim in the text: an asset that needs protecting
  is an asset an adversary may attack; the strict-objective/asset distinction is kept as
  *one end of a tiered measurement*, not as the only measurement.
- The vehicle-twin review (record 59) is excluded from all grid claims; every "one study"
  statement is replaced by "no grid study," and the strict-scope sensitivity (flaw 9)
  removes the record outright.
- "Both = 0" is now labelled a statement about explicit articulation, not evidence that
  dual-role practice is absent.
- The §6.2-vs-conclusion contradiction is resolved: the conclusion now says the review
  "measures only the narrowest, strict-objective instance of its attack-surface axis at
  grid scale and finds that instance empty, while the looser tiers show the twin's
  surfaces widely engaged but almost always defensively. The broader attack-surface axis
  remains untested here." §1 positioning matches.

## Fatal flaw 5 — circular false-negative audit; tie-break artefact

**Required:** independent full-text re-read of a random sample of the 48 negatives;
miss-rate estimate for score-1 mentions; report the 15 weak firings.

**Done: the audit is reframed as disclosure, not evidence; all undisclosed limits are now
disclosed. The full-text re-read itself cannot be executed from the released package (the
PDFs are not redistributable), so it is specified as required future work.**

- §4.9 and §5.8 now state the circularity in the reviewer's terms: the audit is a pattern
  set applied to the output of a pattern-assisted extraction; "no engagement" partly means
  "no keyword hit."
- Recall on score-1 (mentioned-only) engagement — 24 of the 35 engaged — is stated as
  **never measured**; no score-1 positive control was run.
- The **15 weak firings are reported as not individually inspected**, in the methods and
  again in the results, with the sentence "their unexamined status is part of the audit's
  limit, not an oversight we claim to have covered."
- "The audit bounds but does not eliminate the false-negative channel" is replaced by
  "the false-negative channel is disclosed, not bounded," and the design that would bound
  it (independent re-read of a random sample of the 48, with a miss-rate CI propagated to
  35/83) is specified.
- The adjudication circularity is removed: "No headline field moved, which is the point…
  not an artefact of the tie-break rule" is replaced by "under a coder-1-default tie-break
  this is the expected outcome… adjudication, in this design, is not a test of the
  headline at all." The same correction is made in §6.1 and the conclusion, which no
  longer cite adjudication or the audit as robustness evidence.

## Fatal flaw 6 — reliability study cannot carry the claims

**Required:** PABAK and bias indices; CIs; sample frame; corrected κ reporting.

**Done: computed and reported; the structural limits (author coders, n = 20) are declared
rather than argued away.**

- **PABAK and a bias index (max between-coder marginal difference) are added for every
  field** in Table 8, and the method is defined in §4.7.
- **Bootstrap 95% CIs** replace the previous asymptotic intervals for the two collapses
  (any-vs-none 0.60 [0.20, 0.90]; substantive 0.14 [−0.23, 0.64]) and are quoted for
  `twin_role` (0.77 [0.00, 1.00]) and `attack_surface_named` (0.14 [−0.19, 0.49]).
- The 0.41-vs-0.60 conflation is fixed: the text now says the count 35/83 rests on the
  any-vs-none collapse (κ = 0.60) while 0.41 is the three-class κ, and flags that earlier
  drafts conflated them.
- The sample frame is stated: **20 of the 83 full-text records (24%)**, not "20% of 100."
- Both coders are stated to be authors of the review; coder 1 is the codebook author who
  coded 80% of the corpus.
- `twin_role`'s κ is now explicitly uninformative about the rare target class (≈0.2
  expected cases in the sample; CI 0.00–1.00).
- "Symmetric disagreement so no evidence of undercount" is replaced: four disagreements
  cannot distinguish bias from noise, and symmetry is not evidence of accuracy.
- The default-category explanation is no longer asserted: it is quantified by the bias
  indices (maturity 0.35, stance 0.30, attack_surface 0.30), with PABAK alongside κ.
- The threat-vocabulary reliability problem (exact 5%, Jaccard 0.43, mean |Δ| 1.8) is now
  attached to Table 4 and Figure 4 where those numbers are used, with an explicit "least
  reliable data in the review" warning.
- A second independent coder double-coding ≥50% of the corpus is acknowledged as the real
  requirement and is listed as the limiting factor for every headline claim; the
  misclassification sensitivity (flaw 7) is labelled a consistency check for exactly this
  reason.

## Fatal flaw 7 — Wilson intervals meaningless; "bounds" never computed

**Required:** drop the Wilson intervals or replace with misclassification-adjusted
intervals.

**Done: dropped, and replaced.**

- All Wilson intervals are removed from §5.5 and the "bounds, not population estimates"
  sentence is removed from the abstract.
- Replaced with a **misclassification propagation**: assuming coder 2's coding is the gold
  standard, 35 × 7/9 + 48 × 2/11 ≈ **36 of 83 (43.3%)**, bootstrap 95% CI **[21, 51]** —
  i.e. ±15 records — reported in §5.7, the abstract, §6.1 and the conclusion, with the
  caveat that coder 2 is a co-author (consistency check, not validation).
- §8.4 states that no sampling-theory interval (Wilson or otherwise) is reported on a
  ranked census, and names the misclassification sensitivity as the only interval
  attached to the headline.

## Fatal flaw 8 — Table 1 / Habeeb mapping contradicts its text

**Done.**

- The "six additional terms that their query could not return" sentence is gone. The
  bridge section now says the search (not the vocabulary) adds retrieval operators their
  query lacks, that LLM-specific (4) and agentic (2) constructs fall **outside** their
  five vectors, and that the remaining added terms map onto their own vectors — reported
  as coverage, not novelty.
- `dos`, `fdi` and `false_command` are footnoted in the table as classical (non-AI)
  attacks placed by exploited surface.
- The table caption states the mapping is vocabulary-level, a single-author judgment, not
  double-coded, and not evidence of empirical treatment.
- "Designed before we read their paper" is reworded to a claim resting on the dated
  repository log, explicitly not verifiable from the text alone.

## Fatal flaw 9 — scope broader than the abstract says

**Required:** strict-scope treatment; reframe the 17% figure.

**Done.**

- §4.3 now defines the grid term explicitly (grid/power/energy) and lists the records it
  admits: the four out-of-scope records (18 network traffic, 59 vehicle, 69 fraud, 97
  nuclear PPS) and the three borderline ones (34 nuclear DT, 68 education, 84
  battery-telecom).
- A **strict-scope sensitivity** is reported with the headline: excluding the four →
  n = 79: 33 (41.8%) any, 10 (12.7%) substantive, strict target 0; excluding all seven →
  n = 76: 32 (42.1%) any, 10 (13.2%) substantive. The direction is robust; the magnitude
  moves ≤1.5 points. The abstract, §5.5 and the conclusion all carry the strict-grid
  reading.
- The 17% no-full-text figure is reframed as **an access limitation of the authors**, not
  a reproducibility finding, in §4.5, §8.4 and the README.

---

## Presentation and writing points

| Point | Action |
|---|---|
| "AI-Powered Era" title not matched by evidence | Dropped from the title; offensive-AI emphasis deflated; concentration disclosed (one review [ref50] supplies every substantive evasion and agentic case and half the substantive LLM cases) |
| "AI-enabled threat" lumps adversary-uses-AI with attacks-on-AI | Construct split defined in §2.3; notes-based classification of the 11 substantive studies (4 AI-wielded, 5 AI-attacked, 2 both) in §5.5; lumping declared a construct limitation in §8.1 |
| Table 5 IDs vs reference numbers | "Ref." column added; caption states IDs double as bibliography keys |
| 100 studies not listed; reference list held only 27 | New Appendix A lists all 100 (ID, first author, year, venue, FT flag, DOI); `\nocite{*}` puts all corpus entries in the reference list |
| Fig 4 design column empty though a design study exists | Caption and text explain: the single design record names only an out-of-vocabulary threat (`other`), so no vocabulary row registers |
| Maintenance column empty, never discussed | Discussed: no record coded at maintenance or decommissioning; codebook permits both; stated as a finding of the coding with the κ caveat |
| Lifecycle (κ = 0.32) promoted to "the deeper problem"/contribution/P2 | Demoted: removed from the contributions list; §6.3 retitled "read carefully" and marked descriptive-only; P2 reframed as "measure, then extend" with a re-measurement condition |
| Transmission under-represented beside 47 "multi" | Softened: "among the 29 records naming a single domain… wide uncertainty… an observation within this corpus rather than a claim about the literature" |
| Hypothesis from early reading, no threshold | Stated in §1 and §4.1: formed from early reading of part of the same corpus, no pre-specified threshold, analysis exploratory |
| Agenda generic; P3/P5 not AI-specific; nothing that would falsify | Every item now carries confirm **and** disconfirm criteria; P3 specifies attacks on the twin's learned components; P5 specifies releasing models, training data and attack generators |
| "Jôrgensen" encoding error | Fixed to "Jørgensen" in all data files and the bibliography; `gen_bib.py` now transliterates T1-unrenderable characters and escapes venue types (the unescaped `book_chapter` underscore had also broken BibTeX) |
| "Author Onea,∗" artefact | Placeholder restructured (no `\corref` on the placeholder) |
| "baselines/metrics counted over reviews" | Both denominators reported at first mention (41/83 vs 37/49; 43/83 vs 40/49) |

---

## What this revision does *not* fix (and says so)

1. **Coding all 492 eligible records** — impossible from the released package (the 492
   export does not exist in it); specified in `SEARCH_PROVENANCE.md` as the upgrade path.
2. **Probe provenance rebuild** — the original query strings were not preserved; a
   re-execution would not reproduce the original pool and was additionally blocked by
   API rate limits during this revision. Declared, not defended.
3. **Independent full-text re-read of the 48 negatives** — the full texts are not
   redistributable with the package. Specified as required future work in §5.8.
4. **A genuinely independent second coder at ≥50% coverage** — the released reliability
   data come from two authors; every headline claim now carries this limitation
   explicitly instead of citing adjudication or the audit as mitigation.

## Files changed

- `manuscript.tex` — restructured (title, abstract, methods, results, discussion, agenda,
  validity, conclusion, highlights; new tiered-twin table, year-wise table, expanded
  denominator table, expanded reliability table with PABAK/bias, Ref column in Table 6,
  Appendix A input)
- `appendix_corpus.tex` — **new**, auto-generated (all 100 included studies)
- `figures/make_figures.py`, `figures/fig1_prisma.*` — honest flow (Selection not
  Eligibility; probes annotation); script paths made portable
- `gen_bib.py` — T1-safe transliteration, venue-type escaping, portable path
- `included.bib` — regenerated (Jørgensen fix, LaTeX-safe entries)
- `SEARCH_PROVENANCE.md` — **new**, provenance gap manifest
- `analysis/RESULTS.md` — all new sensitivity numbers appended
- `README.md`, `highlights.txt`, `PAPER_PLAN.md` — retitled/reframed; caveats updated
- Data files (`extraction_matrix.csv`, `digital_twin_grid_cybersecurity_papers.csv`,
  `downloads_manifest.csv`, reliability sheets) — Jørgensen encoding fix only; **no codes
  were changed**
- `analysis/*.py`, `figures/make_figures.py` — hard-coded `/mnt/drive2/newpaper` ROOTs
  made repository-relative
- `manuscript.pdf` — rebuilt (tectonic, 56 pp., clean)
