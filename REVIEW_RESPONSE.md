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

---

# Response to the round-4 review

**Decision addressed:** "Major revision. The paper is unusually candid about its limits...
The problem is that the headline claim is framed more strongly than the paper's own
evidence allows, and several design choices make the key nulls close to guaranteed."

**What was done.** This round is a framing-and-consistency revision built on verified
recomputation. Every number added below was recomputed from the released coder sheets and
extraction matrix (`analysis/reliability_round4.py`), every venue/author correction was
verified against Crossref or OSTI on 2026-10-19, and the rebuilt `manuscript.pdf` (61 pp.)
compiles cleanly. The reviewer's bottom line is adopted as the paper's stated contribution:
*the defensible finding is a transparent, small-sample measurement that AI-threat
engagement in grid digital-twin security papers is mostly shallow; the twin-as-target and
lifecycle results are descriptive observations of the coding, not findings about the
field.*

## Major concern 1 — the "asymmetry" headline

**Required:** stop saying "minority engagement"/"rarely" at the any level; make the
substantive count the load-bearing number with its κ = 0.14 fragility; note the
misclassification interval (21–51 of 83, ≈25–61%) straddles 50%; acknowledge the missing
baseline and the same-corpus hypothesis.

**Done.**
- Abstract, §5.5, §6.1 and the conclusion now state it directly: any-level engagement is
  **majority** in the core subsets (16/29 = 55%; 30/55 = 55%); what is minority is
  *substantive* engagement; "any" can mean fewer than two sentences; the substantive count
  is load-bearing and sits on the weakest collapse (κ = 0.14); the 21–51 interval
  includes both minority and majority readings of the any-level share.
- §1 adds: "uses ML for detection" and "engages an AI-enabled threat" are different
  constructs, so there is no normative baseline; the hypothesis came from the same corpus;
  the claim is one of emphasis *and depth*, not rate. The abstract opens with the
  exploratory framing to match §1.
- §3.3's "rarely, and rarely substantively" is replaced by "any-level engagement is
  common---majority in the core subsets---while substantive engagement is the minority
  case"; §6.1's "large defensive apparatus ... rarely studies" is rewritten as a
  within-corpus statement with "rarely examine ... substantively."

## Major concern 2 — definitional null and overreaching loose tier

**Required:** present the strict-target zero as expected-by-design; relabel the 56/83 tier;
note that the only strict-target and only design-phase records are out-of-domain.

**Done.**
- §5.4, Table 3's caption, §6.2 and the conclusion now label the tier counts **descriptive
  observations of the coding, not findings about the field**; §6.2 states that the
  codebook's strict rule makes zero the expected result in a security setting.
- The 56/83 tier is qualified in §5.4, Table 3 and §6.2: the interface threats (MITM,
  replay, false command, reverse pathway) are classical grid-communication attacks that
  any twin-based defender would name; the tier measures threat-*naming*, not that the
  twin's surface is the study's analytical object.
- §5.4 and §6.3 now state that the single strict-target record (R59) and the single
  design-phase record (R97) are both outside the grid domain, so both headline zeros rest
  on out-of-scope records; within a strict grid scope no record is coded at design.

## Major concern 3 — prevalence support and the selection-bias story

**Required:** reconcile §4.3 with §8.5 and the corpus composition; say whether ID equals
rank; archive query strings; add a second database; code the 492.

**Done (partially, with the remainder specified).**
- **The internal contradiction is fixed and its direction established from data:** record
  IDs *are* the retained rank order (verified: IDs 1–45 are all 2026 and citations descend
  within every year block; 40/100 records have zero citations). §4.3 and §8.5 now say the
  same thing: the three ranking components pull in opposite directions and the realised
  rule is **recency-dominant with citations as a tie-breaker**, so foundational 2020–2023
  work is under-represented; the earlier draft's "favours established, cited work" is
  retracted as contradicted by the corpus's own composition. Appendix A's caption and
  intro disclose the ID-order semantics.
- **Strings archived, second database added:** `analysis/search_snapshot_2026-10-19/`
  contains 16 *reconstructed* query strings (12 core + 4 probes, clearly marked as
  reconstructions because the originals were not preserved), a dated Crossref
  (second-database) run of each string with the top-100 results per query, and a README
  stating exactly what the snapshot is and is not. An OpenAlex re-run was **attempted** on
  2026-10-19 and blocked by the shared-IP API budget ("Insufficient budget ... resets at
  midnight UTC"); this is disclosed in §4.2 rather than glossed.
- **Coding the 492:** not possible from the released package (the 492-record export is not
  in the repository; SEARCH_PROVENANCE.md item 4 specifies it as the required artifact).
  The upgrade path remains stated, not asserted.

## Major concern 4 — the abstract-only exclusion falls on the attack side

**Required:** obtain R91/R92 (OSTI, openly hosted) or code twin_role from abstracts and
report a sensitivity analysis; the 17 missing records are not random.

**Done: abstract-level coding + sensitivity analysis.**
- Both OSTI records were retrieved at abstract level (OSTI biblio pages for
  10.2172/2337610 and 10.2172/2331253). R91 is an attack-surface analysis *with attack
  demonstration* on the twin's sensor/instrumentation interface; R92 develops a response
  strategy against **hyperparameter attacks on the twin's own ML models**. Both are
  nuclear-domain (advanced reactors / NPP), i.e. outside the strict grid scope.
- §4.5 now reports the abstract-level twin_role coding of all 17: 15 read as *tool*; the
  two exceptions (R91, R92) read as attack-side work in which the twin's interface and the
  twin's ML models are the object of the attack. The strict-target null now carries an
  explicit "grid-domain, full-text" qualifier wherever it is quoted (abstract, §5.4, §6.2,
  §8.4, conclusion), and §8.4 states that the 17 are not a random subset.
- Full-text retrieval: a direct download was attempted and timed out from this
  environment; the manuscript states that these full texts are openly hosted and that
  retrieving and coding them is required before the null is quoted without the qualifier.

## Major concern 5 — reliability design too thin

**Required:** weighted κ or Gwet's AC1 on the 3-level scale; report threat vocabulary at
the family level or drop the heatmap; independent coder, n ≥ 50, third-party adjudicator.

**Done (statistics added; design upgrades specified as preconditions).**
- **Ordinal statistics computed and reported** (§5.6, abstract, Table 5): linear weighted
  κ = 0.43 (bootstrap 95% CI 0.08–0.74), quadratic weighted κ = 0.44 (0.03–0.80), Gwet's
  AC1 = 0.50 (0.18–0.80) on the 3×3 for `ai_threat_overall`. An **AC1 column was added to
  Table 5 for every field**. §5.6 states the positive classes are thin (each coder: ~9/20
  engaged, 3–4 substantive), so neither κ nor AC1 on the substantive class can be stable.
- **Family-level threat agreement computed and reported** (§5.6): interface family 17/20
  (κ = 0.70), classical family 17/20 (85%, κ = 0.32, prevalence-depressed), learned-model
  family 14/20 (κ = 0.37). Tables 1/2 and Figure 4 are now to be read at the family level;
  per-term counts are indicative only. The heatmap is retained *with* this instruction
  rather than dropped.
- **Design upgrades:** §5.6 now names an independent (non-author) coder, n ≥ 50 enriched
  for engaged records, and a third-party adjudicator as **preconditions for quoting the
  substantive count without its interval** — stated as required work, not achieved. These
  cannot be conjured from the released data; the frozen pre-adjudication sheets remain the
  honest artifact.
- All new statistics are reproducible via `analysis/reliability_round4.py`.

## Major concern 6 — the false-negative audit does not bound the risk

**Required:** acknowledge the 15 uninspected weak firings are cheap to fix; the broad net's
38/48 firing rate shows non-specificity; a blind non-author re-read is feasible now.

**Done (as disclosure, not as new bounds).** §5.7 now states that the 15 uninspected
firings are identifiable from the released audit output and inspectable "in hours, not a
re-design---a resubmission should either inspect them or say why not"; the non-author
re-read is described as feasible for the authors today (full texts in hand) and stated as
the required next test. The 38/48 non-specificity reading is already in §4.7/§5.7 and is
kept. The audit remains a disclosure; no false bound is claimed.

## Major concern 7 — discussion and agenda overreach

**Required:** mark §6.6 and the "large defensive apparatus" sentence as not coded
evidence; flag P2's weak field; make P5 AI-specific; caveat the disconfirmation
conditions; frame abstract/conclusion as exploratory.

**Done.**
- §6.1's apparatus sentence is now explicitly within-corpus and depth-framed (see
  concern 1); §6.6 already carried "author readings, not coded evidence" and keeps it.
- P2 now says the gap is "a coding observation first and a field observation only
  provisionally" and quotes κ = 0.32, AC1 0.54.
- P5 is retitled "Release the learned models, training data and attack generators, not
  just simulation scripts" (title, body and Table 6 row).
- The agenda's intro adds the requested caveat: "primary studies already do this" can be
  revealed by better retrieval as easily as by new science, because the corpus has a
  documented retrieval gap; the same note closes the conclusion.
- Abstract and conclusion now open with the exploratory framing matching §1.

## Internal inconsistencies — all fixed

| Issue | Fix |
|---|---|
| lifecycle "lowest interpretable agreement" vs `attack_surface_named` κ = 0.14 | Reworded everywhere (abstract, §5.4, §6.3, highlights, conclusion): `attack_surface_named` is the weakest field **on both statistics** (κ 0.14, AC1 0.31); lifecycle is reported as moderate (κ 0.32, AC1 0.54) with no "lowest" claim — on AC1, eval_method (0.38) and maturity (0.41) are in fact lower |
| §5.5 "never exceeds 22% in any year" vs 2022 = 1/2 | Now: in years with ≥5 records (2024–26) substantive engagement never exceeds 22%; 2022 (1/2, 50%) is named as uninterpretable on its denominator |
| §5.5 "ML near-universal from 2022" vs 2023 = 4/6 | Now: ML use is 86%+ from 2024; 2023 is 4 of 6 |
| "half the substantive LLM cases (2 of 4)" mixes levels | Now: one of the two substantive LLM cases sits in [50], the other in [16]; at any level 3 of 4 LLM-engaged records are reviews |
| R69 out-of-scope, no strict-scope sensitivity for the 29-subset | Added (§5.5): strict scope inside the core subset removes R18 and R69 → 27 studies, 15 (55.6%) any, 5 (18.5%) substantive; 25 studies (14 any, 5 substantive) if borderline records are also removed |
| ~700 probe-added vs "469-record probe pool" | Reconciled by disclosure (§5.5, §8.2): the 24/469 figure comes from an earlier abstract-level scan whose per-record artifact was not preserved; its relation to the ~700 probe-added candidates is not established; it is now treated as an unreproducible working number, and its 5% hit rate is read as evidence the probes were largely non-specific |
| §1.1 "had to be repositioned" vs §3.2 "designed independently" | §3.2 now separates the two claims: the vocabulary predates reading their review per the dated design log (unverifiable from the text alone); the *positioning* was revised after reading it. The stronger independence claim is withdrawn |
| "62 journal articles" includes Zenodo/IRJMETS | §5.8 replaces the venue-type filter with a **peer-review-filtered sensitivity**: 62 journal-classified full-text records minus R30, R32 (Zenodo), R65 (GSC Online Press), R69 (IRJMETS) → 58 records: 23/58 (39.7%) any, 8/58 (13.8%) substantive, 35/58 none, 55/58 tool, 1 targeted (the out-of-domain R59). §8.7 notes the venue-type filter is not a peer-review certification; the denominator table gains the 58-row |
| "[18, 19]" citations vs "records 18, 59..." | Corpus records are now cited as **R18, R59, R69, R97, R30, R32, R34, R65, R68, R84, R91, R92** etc. throughout; Appendix A defines the R-notation and its relation to bibliography keys, and notes that rendered reference numbers do not equal record IDs |
| "Appendix 9" | Root cause fixed: `\ref` inside the starred appendix section resolved to the section counter. All references now hardcode "Appendix A" |
| future-work pointer cycles §5.8 ↔ §8 | Cycle broken: §3.7 points to §5.8; §5.8 is self-contained ("stated here as the required next test") and no longer points to §8 |
| Tables 8–9 float after the references | `\clearpage` added before the bibliography; verified in the rebuilt PDF: Table 8 and Table 9 now render before the reference list |
| reference hygiene (garbled [44], [54], [85], [91]; "Authors unreported"; affiliation-as-authors [81]; unknown venues) | Fixed at source and in `gen_bib.py`: Cyrillic author names transliterated (R25 Loskutov/Kulikov, R36 Petrenko, R75 initials); affiliation fragments "Zap. Kaz. REC" and "QHSE-AKBARYS" removed from R75 (Crossref-verified author list); curly apostrophe normalised (R79 "Network's"); `USDOE` dropped from R91/R92 author lists; comma-separated author lists parsed (R32 now has its authors); venues verified via Crossref/OSTI for R26 (West Virginia University), R27 (IEEE PARC 2026), R40 (Wiley, *AI and Digital Twins Under Siege*; reclassified report → book chapter, profile counts updated 3 reports/4 chapters), R72 (ICTAACS 2025), R91/R92 (Idaho National Laboratory/OSTI), R99 (Florida International University). The only remaining "Authors unreported" is R69 (IRJMETS), which is genuinely unattributed. The regenerated `included.bib` renders without mojibake (verified in the PDF) |

## What this revision does not fix (and says so in the manuscript)

1. **The original 16 OpenAlex query strings and per-record provenance** — not in the
   released record; reconstructed strings + dated Crossref snapshot archived instead;
   OpenAlex re-run attempted and blocked by the shared-IP budget.
2. **Coding the 492 eligible records or a random sample of them** — the 492-record export
   is not in the package; specified as the required artifact in `SEARCH_PROVENANCE.md`.
3. **An independent coder, a ≥50-record enriched sample, a third-party adjudicator, and
   the blind non-author re-read of the 48 negatives** — require human coders and the
   non-redistributable full texts; stated as preconditions/required next tests, not
   claimed as done.
4. **Full-text coding of R91/R92** — abstract-level coding and sensitivity analysis
   provided; retrieval attempted, timed out from this environment; the reports are openly
   hosted and the manuscript says the coding must be completed before the strict-target
   null is quoted unqualified.

## Files changed this round

- `manuscript.tex` — abstract, §1, §3.2, §3.3, §4.2, §4.3, §4.5, §5.2, §5.4, §5.5, §5.6
  (weighted κ, AC1, family-level agreement, design preconditions), §5.7, §5.8
  (peer-review-filtered sensitivity), §6.1–§6.3, §7 (P2, P5, disconfirmation caveat),
  §8.2, §8.4, §8.5, §8.7, conclusion, highlights, R-notation, Appendix-A references,
  float flush
- `appendix_corpus.tex` — R-notation, ID-order disclosure, verified venues for R26, R27,
  R40, R72, R91, R92, R99
- `analysis/reliability_round4.py` — **new**, reproduces every statistic added this round
- `analysis/search_snapshot_2026-10-19/` — **new**, reconstructed strings + dated Crossref
  second-database snapshot (16 query CSVs + `queries.json` + README)
- `gen_bib.py` — Cyrillic transliteration, curly-quote/dotless-ı mapping, org-token
  filter, comma-separated author parsing, type-label deduplication
- `included.bib` — regenerated (clean rendering verified)
- `analysis/extraction_matrix.csv`, `digital_twin_grid_cybersecurity_papers.csv` —
  Crossref/OSTI-verified author and venue corrections (R25, R26, R27, R36, R40, R72, R75,
  R79, R91, R92, R99) and R40 venue_type report → book_chapter; **no codes were changed**
- `highlights.txt`, `README.md` — reframed to the shallowness finding
- `SEARCH_PROVENANCE.md` — snapshot reference and 24/469 provenance note
- `analysis/RESULTS.md`, `analysis/summarise.py` — 469 figure marked as unpreserved;
  round-4 numbers appended
- `manuscript.pdf` — rebuilt (tectonic, 61 pp., clean; Tables 8–9 before references; no
  mojibake)
