# Revision notes — third-round editorial and reporting repairs

This branch repairs the faults carried over from the two peer-review rounds
(`peer review.docx`, `peerreview2.docx`, `peerreview3.docx`) plus defects found in an
independent full-document re-verification against `analysis/extraction_matrix.csv`.
No headline number changed: every quantitative claim in the manuscript was recomputed
from the matrix and the coder sheets, and all of them reproduce. The changes are
reporting, cross-referencing, statistics, and reproducibility repairs.

## A. Faults fixed in the abstract

1. **Garbled reliability sentence** (round 2, §2.2; round 2 minor item 1). The sentence
   "Two coders agreed on 35/83 at κ = 0.60 … and one of six at κ = 0.14" conflated the
   20-study agreement sample with the 83-study corpus counts. Replaced with the
   reviewer's suggested form: agreement is now reported as 16/20 (κ = 0.60) for
   any-versus-none and 15/20 (κ = 0.14, one shared substantive label of six) for
   substantive-versus-not, with the corpus-level figures explicitly framed as bounds.
2. **Missing probe disclosure** (round 2, §5.2). The abstract now states that the
   1,287 core records were widened by four adversarial-AI probe queries to a candidate
   pool of roughly 2,000.
3. **Misplaced κ = 0.32 parenthetical.** The abstract attached "(κ = 0.32)" to
   "none at commissioning"; it is the lifecycle-stage coder agreement and is now
   labelled as such.
4. **Looser twin-as-target definition** (round 2, §5.4). The abstract now discloses
   that the count under a looser asset-under-protection definition is uncomputed;
   the Conclusion's "exactly one study" claim now carries the same strict-definition
   qualifier.

## B. Cross-reference and structure repairs

5. **"the Section 5.4 figures"** (§4.3) pointed at the wrong section after the round-2
   renumbering; now a `\ref{sec:ai-threats}` that resolves to 5.5.
6. **"the abstract-versus-full-text comparison in Section~\ref{sec:audit}"** (§6.4)
   pointed at the false-negative audit (5.8) instead of 5.5; the sentence was removed
   together with the 24/469 figure it qualified (item 12 below).
7. **"full scope alignment is in Section 6.2"** (§6.5) was a hard-coded, wrong
   reference; now `\ref{sec:bridge}` (resolves to 3.2, the vocabulary-mapping
   subsection, which now carries a label).
8. **Circular self-reference** in §4.3 ("applied the eligibility rule in
   Section~\ref{sec:method}" — its own parent section) now points to the Screening
   subsection (§4.4) via a new `\label{sec:screening}`.
9. **Float placement** (round 2, minor item 14). The reliability and agenda tables
   (`table*[t]`) overflowed to after the reference list in the compiled PDF. Both are
   now `table[!htbp]` and place inside the body (pages 20 and 24 of 31).

## C. Denominator and vocabulary reconciliation

10. **62 vs 67 journal articles** (round 2, §5.6 and minor item 8; second request).
    Verified from the matrix: the corpus contains 67 journal articles, of which 62 have
    full text (5 are abstract-only). The denominators table row now reads "Journal
    articles (full text)", the ML-used and non-review rows are marked as full-text
    subsets in the caption, the reconciliation is stated in one sentence after the
    table, and the venue-quality sensitivity in §5.6 says "62 full-text journal
    articles" and that it discards 21 of the 83 full-text records.
11. **evasion (11) vs ai_evasion (9)** (round 2, §4.7 vocabulary point). The bridge
    paragraph in §3.2 now marks evasion as the broad threat-vocabulary term (11) and
    gives the AI-specific engagement field count (9) inline.
12. **The 24/469 screening figure removed** (round 2, §5.2 and minor item 9; second
    request). The 469-record probe pool is not part of the released record and its
    denominator is undefined, so the figure supported no inference. Removed from all
    three locations (§5.5, §6.4, §8.2); §5.5 and §8.2 now state the defensible,
    directional point: abstract-level screening under-counts AI-threat engagement
    relative to full-text coding, by an unquantified amount.
13. **"and its direction"** (round 1, carried item) — the unexplained phrase attached
    to the 17% unobtainability rate was deleted.

## D. Statistics added from the released data

14. **Fisher exact tests** (round 1, carried item 9) replace "unsupported by any test":
    review share of the substantive set, 5/11 vs 34/83, p = 1.0 (§5.5 and §6.4); bridge
    share, 3/11 vs 8/83, p = 0.12 — the §6.4 claim "bridge studies are
    [over-represented]" is accordingly softened to "more prevalent … not significant
    at this n" (§6.4).
15. **Wilson 95% intervals** (round 1, carried item) now accompany the remaining
    headline proportions: twin-as-target 1/83 (0–7%, §5.3), operation 66/83
    (70–87%, §5.4), explicit threat model 19/83 (15–33%) and adaptive adversary
    10/83 (7–21%, §5.4).
16. **ml_family agreement figure** in the reliability table corrected to "Jaccard 0.30
    (0.42 norm.)" — the raw set score, matching `analysis/reliability/AGREEMENT.md`;
    the previous 0.42 was the post-normalisation value reported without qualification.
17. **Re-verification of everything else.** The 3×3 agreement table, both collapsed κ
    values (0.60, 0.14), their asymptotic intervals ([0.24, 0.95], [-0.52, 0.79]), the
    three Wilson intervals in §5.5 (32–53, 8–22, 47–68), all corpus decompositions
    (stance, twin role, lifecycle, evaluation method, years, venue types, publishers),
    the per-vector AI-threat counts, the 11-substantive-study table, and the
    venue/non-review sensitivities all reproduce exactly from the released matrix and
    coder sheets (`analysis/reliability_agreement.py` runs unchanged after the path
    fix below).

## E. Reporting completeness

18. **Search cutoff stated** (round 2, minor item 11; second request). §4.2 now states
    that the corpus was frozen on 16 October 2026 and that this date is the search
    cutoff; §8.4's limitation list drops "no stated search date in the text" and
    points to the stated cutoff instead.
19. **Retrospective codebook application** (round 2, minor item 10). §4.6 confirms in
    one sentence that revisions R2–R6 were applied retrospectively to all 100 records.
20. **Corpus-record citation convention** (round 2, minor item 15; second request).
    §4.5 states the convention: bracketed citations of corpus records resolve to that
    record's own bibliographic entry; table ID columns carry the record numbers.
21. **Highlights** are now five bullets, each ≤85 characters (Elsevier requirement),
    synced between `manuscript.tex` and `highlights.txt`; the "(fragile)" calibration
    flag is retained on the substantive-engagement bullet.
22. **Coder-1 coverage** in §6.3 is now precise: "sole coder for 80 of the 100
    records" (the double-coded sample is 20; 100 − 20 = 80), replacing the ambiguous
    "coded 80% of the corpus".
23. **Publisher-label caveat** added to §5.2: 42 of 100 records carry no publisher
    label in the source metadata, so publisher counts are over labelled records only.
24. **Figure 4 verification** (round 2, minor item 6). The insider and supply-chain
    rows were re-derived from the matrix (20 and 19 records respectively, matching
    Table 4) and the figure was regenerated from the released script; the suspected
    transposition was a PDF text-extraction artifact, as the reviewer anticipated.

## F. Reproducibility repairs

25. **All analysis scripts now auto-detect the repository root** from their own
    location (override with the `DTGRID_ROOT` environment variable). The previous
    hard-coded `/mnt/drive2/newpaper` path made every script fail on any other
    machine. Affected: `figures/make_figures.py`, `gen_bib.py`, and all eight
    `analysis/*.py` scripts.
26. **`figures/make_figures.py` docstring corrected** ("every number is read from the
    matrix" was false for Figure 1, whose flow counts come from `prisma_flow.txt`),
    and the Figure 3 screening-seed bars are now derived from the matrix's
    `stance_seed_from_openalex_screening` column instead of a hard-coded dict
    (values identical).
27. **All five figures regenerate byte-comparable** from the current script + matrix
    (verified; committed binaries left untouched to avoid version-noise diffs).

## G. Known items deliberately not changed

- **Author list, affiliation, and email remain placeholders** — a submission-time
  decision tied to the Research4Life corresponding-author constraint, flagged in the
  source comments and README.
- **Probe-only membership among the retained 100 is still not computable** from the
  released data (the corpus CSV carries no per-record query provenance). §4.3 and
  §8.5 keep the honest disclosure; §8.5 now states the reason (no query provenance in
  the released dataset) rather than promising a future fix.
- **The non-probabilistic top-100 selection rule** is disclosed, not changed —
  re-running the selection with a published formula or alternative cuts requires the
  unreleased OpenAlex retrieval outputs, not the released matrix.
- **lifecycle_stage re-coding and the looser twin-role coding** require re-reading the
  83 full texts, which are not redistributable; the caveats (κ = 0.32, default-category
  bias, uncomputed looser count) are carried consistently instead.
