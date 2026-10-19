# Paper Plan — Digital Twins for Cyber-Resilient Power Grids

Status: execution started. Corpus frozen at 100 records.
Last updated: 2026-10-16

> **Revision history.** This plan predates the review rounds and still describes the
> paper as a "systematic review" with an "AI-Powered Era" framing; both were withdrawn in
> the round-3 revision (2026-10-19). The paper is now a *structured corpus review* (ranked
> top-100 subset, PRISMA-flow reporting only), with claims re-derived on matched
> denominators, tiered twin counts, strict-scope sensitivity analysis, PABAK/bias
> reliability statistics, and a misclassification sensitivity in place of Wilson
> intervals.
>
> The round-4 revision (2026-10-19) re-framed the headline: any-level engagement is
> majority in the core subsets, so the defensible finding is that engagement is *common
> but shallow*; twin-as-target and lifecycle results are descriptive observations of the
> coding, not field findings. Reliability reporting gained weighted kappa, Gwet's AC1 and
> family-level threat agreement; the venue sensitivity became a peer-review filter
> (n=58); R-notation (R<n>) separates corpus IDs from reference numbers; and a dated
> search snapshot with reconstructed query strings is archived under
> `analysis/search_snapshot_2026-10-19/`.
>
> This file is kept as the historical planning record; see `REVIEW_RESPONSE.md` for the
> point-by-point changes.

---

## 1. What the paper is

**Working title:** Digital Twins for Cyber-Resilient Power Grids: A Systematic Review and a
Research Agenda for the AI-Powered Era

**Type:** systematic literature review (PRISMA 2020) + research agenda. Not an empirical study.

**Central argument (every section serves this):**

> Grid digital-twin security research has adopted AI as a *defensive* tool far faster than it has
> modelled AI — or the twin itself — as an *attack target*. We quantify that asymmetry across a
> screened corpus and set a testable agenda to close it.

⚠️ **Repositioned after reading the competitor (see `analysis/COMPETING_REVIEWS.md`).** Habeeb et al.
(2026) already published a PRISMA review of "Dual-Role Digital Twins" for cyber-physical security
generally. **We cannot claim to have discovered the dual-role tension.** But reading it revealed the
opening: their framework asserts two axes — attack-surface expansion and defence enablement — and
operationalises **only the defence axis**. Their Functional Quadrant Taxonomy (Sandbox, Sensor,
Honeypot, Ledger) classifies all 20 of their studies into defensive roles, and their search string
contains no attack-side operator at all. The attack axis survives as one algebraic term and a list
of five vectors.

**Lead framing:** *the dual-role framework operationalises one of its two axes; we supply the other,
at grid scale, with reported reliability.* This is a theory-testing review answering a theory-building
one. Their contribution is a construct; ours is the measurement of it.

**Contributions**

| # | Contribution | Evidence artefact | Status |
|---|---|---|---|
| C1 | PRISMA-screened, DOI-verified corpus of 100 studies (2020–2026), openly released | `downloads_manifest.csv`, `analysis/doi_verification_all.csv` | built |
| C2 | Stance taxonomy — the **attack axis** the competing framework left as a scalar | `analysis/codebook.md` §2.1 | built |
| C3 | Grid-specific measurement of the adversarial-vs-defensive asymmetry, with inter-rater reliability | `analysis/extraction_matrix.csv` | needs Phase B |
| C4 | Application of the competitor's **five attack vectors** to 100 grid studies — which are populated, which are empty | `extraction_matrix.csv` (`threat_models_named`) | needs Phase B |
| C5 | Quantified engagement with **AI-enabled** threats (evasion, poisoning, LLM, agentic) on a 0/1/2 scale | `extraction_matrix.csv` | needs Phase B |
| C6 | Lifecycle-stage coverage — answering the competitor's first named research gap | `extraction_matrix.csv` (`lifecycle_stage`) | needs Phase B |
| C7 | Prioritised research agenda with testable propositions P1–P5 | manuscript §6 | pending |

### Research questions

Deliberately distinct from the competitor's four. Theirs map the construct; ours test it.

- **RQ1 — Corpus.** What is the shape of grid digital-twin security research, 2020–2026 (volume,
  venues, maturity, evaluation rigour)?
- **RQ2 — Axis balance.** Do grid studies distribute symmetrically across the attack and defence
  axes their framework postulates, or does one dominate?
- **RQ3 — Vector coverage.** Of the five attack vectors named in the competing framework, which are
  populated in the grid corpus and which are empty?
- **RQ4 — AI-era engagement.** To what extent does the corpus engage AI as an *attacker* — evasion,
  poisoning, adversarial ML, LLM and agentic vectors — as opposed to only as a defensive tool?
- **RQ5 — Lifecycle.** Which lifecycle stages does the research protect, and which are unaddressed?

---

## 2. Target venue

**Primary: International Journal of Critical Infrastructure Protection (Elsevier), hybrid.**

Rationale: scope is literally critical-infrastructure cyber-physical protection; it publishes
systematic reviews; the digital-twin-as-attack-surface argument lands inside its remit.

**Cost = $0, two independent routes** (Bangladesh is Research4Life **Group A**; both Elsevier and
Wiley list Bangladesh in their APC waiver/discount lists):

- Publish **non-OA** in the hybrid journal → no APC exists on the subscription route.
- Publish **gold OA** with the R4L Group A waiver → waived.

Deliberately avoided: IEEE Access (~$1,800, no Bangladesh-wide waiver) and MDPI (discretionary
waivers, not country-guaranteed). Both put real money at risk.

**Critical constraint:** the waiver attaches to the **corresponding author's institution**, not to
the author personally. The corresponding author must be affiliated with a Bangladeshi institution.
Decide this before submission.

**Fallback ladder (same waiver mechanics):**

1. *Sustainable Energy, Grids and Networks* (Elsevier) — if grid framing must dominate
2. *Computers & Security* (Elsevier) — higher prestige, harder
3. *IET Smart Grid* (Wiley, gold OA) — fastest, lower signal

**Consequences of the Elsevier target:**
- Numbered citation style; ~9,000–10,000 words.
- **5 Highlights of ≤85 characters** — draft early, they are the thesis in five lines.
- Figures at 300 dpi. Do *not* use the IEEE SVG template; generate with matplotlib to Elsevier specs.
- Post to **arXiv first** (free, timestamped, priority against the competing-review risk).

---

## 3. Frozen corpus

Screening is complete and frozen. No changes after coding starts.

```
IDENTIFICATION   1,287 unique works (12 core OpenAlex queries; +adversarial-AI probes)
SCREENING        492 eligible   (795 excluded: no digital-twin term, or no grid domain)
ELIGIBILITY      100 retained   (relevance + citations + recency)
INCLUDED         100 papers     | 83 full texts on disk | 17 abstract-only
```

Stance distribution — **screening seed**: defensive 42 · review 23 · enabling 15 · adversarial 11 ·
bridge 9. **Adjudicated coding (all 100)**: defensive 42 · review 36 · bridge 10 · enabling 10 ·
adversarial 2. The shift is a screening finding, reported in §4/§7 (see `analysis/RESULTS.md`).

**Two denominators, never mixed.** Full-text-coded fields are n=83; metadata/abstract fields are
n=100. Every table states its denominator; abstract-only records are flagged.

---

## 4. Phases

### Phase A — Protocol and setup (week 1)
- [x] Freeze corpus at 100
- [x] Write codebook (`analysis/codebook.md`)
- [x] Build extraction matrix scaffold (`analysis/extraction_matrix.csv`)
- [x] Draw stratified 20% reliability sample (`analysis/reliability/sample20.csv`)
- [x] Write second-coder instructions (`analysis/CODING_INSTRUCTIONS.md`)
- [x] Verify all 100 DOIs against Crossref/DataCite
- [x] **Novelty check** → direct competitor found, obtained, read, and repositioned around it (§1). Residual risk now low.
- [ ] Register protocol on OSF
- [ ] Map our threat vocabulary onto the competitor's five vectors (table for §4)
- [ ] Confirm corresponding-author arrangement (waiver depends on it)

### Phase B — Full-text extraction (weeks 2–5)
- Extract 83 full-text records against the codebook
- Code the 17 abstract-only records on abstract-level fields only, and flag them
- Second coder independently codes the 20-paper stratified sample
- Compute agreement: Cohen's κ for multi-class fields (target κ ≥ 0.61); **percentage agreement**
  for sparse AI-threat fields (κ is undefined at zero prevalence — see §6)
- Adjudicate disagreements with the first coder

### Phase C — Analysis and figures (weeks 6–7)
| Output | Serves | Source |
|---|---|---|
| Fig 1 PRISMA flow | Method | `prisma_flow.txt` |
| Fig 2 Publication-year histogram + venue types | RQ1 | matrix |
| Fig 3 Stance distribution | RQ2 | matrix |
| Fig 4 Threat-model × twin-component coverage heatmap | RQ2 | matrix — blank cells are the argument |
| Fig 5 AI-threat engagement (0/1/2 per vector) | RQ3 | matrix |
| Table 1 Corpus profile | RQ1 | matrix |
| Table 2 Adversarial vs defensive comparison | RQ2 | matrix |
| Table 3 Studies that do engage AI threats, in detail | RQ3 | matrix |
| Table 4 Gap → direction → validation | RQ4 | synthesis |

Skip keyword co-occurrence / bibliometric mapping: decorates rather than argues.

### Phase D — Drafting (weeks 8–10)

| § | Content | Words |
|---|---|---|
| Abstract + highlights | Structured; asymmetry claim up front | 250 |
| 1 Introduction | Tension → gap → contributions → roadmap | 1,000 |
| 2 Background | DT anatomy; grid threat landscape; prior surveys and how this differs | 1,300 |
| 3 Methodology | Protocol, queries, screening, extraction, codebook, κ, PRISMA disclosure of 17 | 1,500 |
| 4 Results | RQ1 → RQ2 → RQ3, figure-led, no interpretation | 3,000 |
| 5 Discussion | Why defence is tooled but not threat-proofed; twin-trust circularity; implications | 2,000 |
| 6 Research agenda | RQ4; propositions P1–P5 | 1,000 |
| 7 Threats to validity | Abstract-vs-fulltext, 17 missing, English-only, corpus recency | 600 |
| 8 Conclusion | | 400 |

Writing order: Methodology → Results → Discussion → Introduction → Abstract.
The introduction is the last thing that can be written honestly.

### Phase E — Reproducibility package (week 11)
Zenodo DOI containing: corpus CSV · extraction matrix · codebook · screening log · query strings
and run dates · DOI verification log · retrieval manifest · analysis scripts.

---

## 5. Timeline

| Weeks | Work |
|---|---|
| 1 | Protocol → OSF; verify 100 DOIs; novelty check; corresponding-author decision; freeze corpus |
| 2–5 | Full-text extraction (83); abstract-level (17); stratified double-coding + agreement stats |
| 6–7 | Analysis; figures at 300 dpi; Highlights drafted |
| 8–10 | Draft §§3→4→5→6, then 1→2 |
| 11 | Internal read; threats-to-validity; Zenodo package |
| 12 | Submit to IJCIP |

---

## 6. Known traps

1. **The 5.1% figure is abstract-based** (24/469, computed over the wider relevant set). It has now
   been re-derived on the final corpus from **full text** using the 0/1/2 scale (Phase B complete;
   see `analysis/RESULTS.md`). Result: **35/83 = 42.2%** engage any AI-enabled threat at all, and
   **11/83 = 13.3%** engage substantively. The abstract-level figure under-counted engagement by
   roughly a factor of eight. Report both and present the delta as a validity finding: abstract-only
   screening systematically under-counts AI-threat engagement. This turns the weakest number into a
   methodological contribution. Non-negotiable.
2. **Cohen's κ must be read with prevalence.** Early framing assumed the AI-threat fields would
   have zero variance (κ undefined). They do not: the corpus engages adversarial ML (24), poisoning
   (19), evasion (9), LLM (4) and agentic (2) at some level, and `ai_poisoning` returns κ = 0.73.
   κ is undefined only where a category is genuinely constant (`ai_llm`, `ai_agentic`, and the
   near-constant `stance_confidence`/`limitations_stated`/`data_available`). Report **percentage
   agreement** for those and state why. See `analysis/reliability/AGREEMENT.md`.
3. **Novelty — resolved into a _positioning_ risk, not a survival risk.** The 2026 review of
   "Dual-Role Digital Twins" has been read (`analysis/COMPETING_REVIEWS.md`). It is a theory-building
   review of N=20 studies that operationalises only the defence axis and carries no attack-side search
   operator. Our theory-testing, grid-scale measurement complements it. **Do not lead with the
   dual-role framing** — lead with operationalising the axis they left as a scalar. The worst credible
   reviewer response is now "a fair extension", not a novelty rejection.
4. **83/100 full texts.** Disclose everywhere; never describe the corpus as 100 for full-text claims.
5. **Corpus recency:** 76% is 2025–26. Frame as a dated snapshot with a stated search cutoff.
6. **Data anomalies to handle in text:** 3 no-DOI repository records; 1 non-resolving DOI
   (`10.63544/qcr0y085`); 18 venue labels where OpenAlex disagreed with Crossref.

---

## 7. Files

```
PAPER_PLAN.md                              this file
analysis/codebook.md                       coding manual — authoritative field definitions
analysis/CODING_INSTRUCTIONS.md            second-coder brief (standalone, send as-is)
analysis/COMPETING_REVIEWS.md              novelty check + repositioning decision
analysis/extraction_matrix.csv             the matrix — sole source of every table number
analysis/doi_verification_all.csv          Crossref/DataCite verification of all 97 DOIs
analysis/build_matrix.py                   regenerates the matrix + sample from source CSVs
analysis/verify_all_dois.py                verifies every DOI against Crossref, then DataCite
analysis/reliability/sample20.csv          stratified 20% sample (seed 20261016)
analysis/reliability/coder1_sheet.csv      coder 1 workspace (not for coder 2)
analysis/reliability/coder2_sheet.csv      coder 2 workspace — send this one
```
