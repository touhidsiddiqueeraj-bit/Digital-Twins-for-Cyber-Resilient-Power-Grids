# Competitor analysis — the Dual-Role Digital Twins review

> **"From attack surface to security asset: a systematic review of Dual-Role Digital Twins in
> cyber-physical security (2019–2025)"**
> Habeeb, Weli & Almaliki · *Digital Twin* (Taylor & Francis) · 1 June 2026
> DOI `10.1080/27525783.2026.2679856` · Open Access (CC BY-NC)

**Status: full text obtained and read (2026-10-16).** Everything below is verified against the paper,
not inferred from metadata.

---

## 1. What it actually claims

| | |
|---|---|
| Method | PRISMA 2020: **412 identified → 318 screened → 72 eligibility → 20 included** |
| Corpus | **N = 20 studies**, Jan 2019 – Dec 2025 |
| Sources | IEEE Xplore, Scopus, Web of Science, Google Scholar |
| Query | `("Digital Twin" OR "DT") AND ("Cybersecurity" OR "Attack Surface" OR "Defense" OR "Honeypot" OR "Intrusion Detection")` |
| Domains | smart manufacturing, healthcare, IIoT, smart city, water management; **power grid represented in ~1 of 20 studies** |
| Theory | Complex Adaptive Systems, Functional Duality, Zero-Trust Architecture |

**Four research questions**

- **RQ1 Threat landscape** — how DT inclusion extends the attack surface, and *"what classes of
  threat, including data poisoning, exploitation of models, adversarial artificial intelligence, and
  reverse attack vectors, are the most characteristic … 2019 to 2025?"*
- **RQ2 Defence taxonomy** — the **Functional Quadrant Taxonomy: Sandbox, Sensor, Honeypot, Ledger**
- **RQ3 Research gaps** — lifecycle-aware frameworks, large-scale empirical validation, standardised metrics
- **RQ4 Future pathways** — the speculative **"Immune Digital Twin"**

**Their headline contribution** is a *theoretical* construct:

> `W_DT(t) = a · ASE(t) − b · DE[F] + e(t)`

Net security state = attack-surface expansion minus defence enablement, across the DT lifecycle.

**Their five named attack vectors** (this is important — see §3 below): bidirectional data-link
exploitation; adversarial data poisoning on sensor streams; AI/ML model exploitation via
adversarial training-distribution attacks; the **reverse attack pathway** (compromised virtual model
propagates erroneous commands to physical actuators); supply-chain and cross-sector interconnectivity.

---

## 2. Our earlier fears were overstated

The metadata-only assessment said this paper occupied our framing. Having read it, the assessment
softens considerably:

| Our earlier worry | Reality |
|---|---|
| "It already reviews DT cybersecurity" | True, but across **20 studies in four databases** and a **five-term query** |
| "It owns the dual-role framing" | It **names** the duality; it does **not measure** it |
| "It may quantify the adversarial/defensive split" | **It does not.** There is no proportion, no distribution, no coding of attack-vs-defence |
| "It may already cover AI-enabled threats" | It **names** AI threats among five vectors; it reports **zero** engagement with evasion, LLM, agentic or generative attacks |
| "It may already cover power grids" | Roughly **1 of 20** studies touches grids; `electric`/`substation` appear **0 times** |

It is a **theory-building** review. Ours is a **theory-testing** review. Those are complementary, not
competitive — and the difference is the opening.

---

## 3. The framing we can target

Five framings, ranked by strength and defensibility. **F1 is the one to lead with.**

### F1 — Operationalise the axis they left as a scalar ★ lead framing

This is the sharpest and most defensible point, and it is verifiable from their own paper:

1. Their framework has **two axes**: Attack Surface Expansion and Defence Enablement.
2. Their **Functional Quadrant Taxonomy contains only defensive roles** — Sandbox, Sensor,
   Honeypot, Ledger. Their Table 2 classifies **all 20 studies into these four defensive roles**;
   **not one study occupies an attack-side category, because none exists.**
3. The attack axis is therefore present only as (a) one algebraic term, `ASE(t)`, and (b) a list of
   five vectors. **It is never used to classify the literature.**
4. Their **search string contains no attack-side operator** — no `attack`, `adversarial`, `malware`,
   `exploit`, or `threat actor`. Retrieval was structurally defence-weighted, so the attack axis is
   characterised from a narrow base and, unsurprisingly, no attack studies were retrieved to classify.

> **Positioning:** the dual-role framework asserts symmetry between an attack axis and a defence
> axis, then operationalises only the defence axis. We operationalise the attack axis — coding every
> study on both, with reported reliability — and show the two axes are not symmetric at all.

This is generous to them (we treat their model as the starting construct) and it is fatal to any
claim that the field has been mapped. It also gives our stance taxonomy a *reason to exist*: it is
the missing second axis, not a relabelling of their quadrants.

### F2 — Sector baseline before cross-sector generalisation

Their own stated limitation #3: *"no reviewed system was validated at production scale in a
heterogeneous, multi-sector deployment."* Their remedy is cross-sector synthesis.

But their own §1 concedes: *"Each sector's DT adoption carries a distinct security signature."*

> **Positioning:** before a multi-sector model can be validated, each sector needs a baseline.
> This paper supplies the power-grid baseline — the sector where the signature is most severe
> (safety-critical, real-time, kinetic consequences, regulated) and where their corpus offers
> essentially nothing (~1 of 20 studies).

Their own words supply both premises. This is the safest framing in the set.

### F3 — Test their five vectors against 100 grid studies

This is the *method* framing and it makes the paper visibly responsive to theirs. Our codebook's
threat vocabulary maps almost one-to-one onto their five vectors:

| Their vector | Our code |
|---|---|
| (i) Bidirectional data-link exploitation | `mitm`, `replay` |
| (ii) Adversarial data poisoning on sensor streams | `fdi`, `poisoning` |
| (iii) AI/ML model exploitation (training-distribution attacks) | `ai_adv_ml`, `ai_poisoning` |
| (iv) **Reverse attack pathway** (virtual → physical actuators) | **not yet in our codebook — add it** |
| (v) Supply-chain / cross-sector interconnectivity | `supply_chain` |

> **Positioning:** we apply their taxonomy at grid scale and report which vectors are populated and
> which are empty — turning their conceptual list into a measured coverage map.

### F4 — The AI-era window their framework cannot see

Their window closes **Dec 2025**. Their five vectors include adversarial AI, but the corpus contains
**zero** mentions of evasion, LLM, agentic or generative attacks. 76% of our corpus is 2025–26.

> **Positioning:** the vectors that define the current threat environment postdate their window.
> We are not contradicting them — we are extending the same taxonomy into the period where AI
> stopped being a defensive tool and became an attack one.

Careful phrasing required: **do not claim "no one has considered AI threats."** They did name them.
The claim is about *engagement* — whether the research corpus actually studies them — and about the
newer vectors.

### F5 — Answer their explicit call for empirical work

They write, unprompted:

> *"a and b can be estimated from real-world deployment data … empirical validation corresponds to
> estimating the function parameters."*

and their limitation #2 is that AI anomaly detection *"remains vulnerable to adversarial manipulation
of the training distribution itself."*

> **Positioning:** we take the first empirical step at sector scale on the axis where data exists —
> the research community's actual allocation between the two axes.

**Honesty constraint:** we measure **research attention**, not deployment security. We cannot estimate
`a` or `b`. Say so in one sentence; anything else is overclaiming and a reviewer will catch it.

---

## 4. Recommended positioning

Lead with **F1 + F2**, use **F3** as the method, land **F4** as the headline finding, and invoke **F5**
once in the discussion as a hook. Concretely, §2 of our manuscript gets a positioning subsection:

> The dual-role character of digital twins has been formalised for cyber-physical systems generally
> [Habeeb et al. 2026]. That framework rests on two axes — attack-surface expansion and defence
> enablement — but operationalises only the latter: its taxonomy classifies defensive roles, and its
> retrieval strategy contains no attack-side operator. We take up the model and supply the missing
> half, at sector scale, for power grids.

That is defensible, respectful, and it converts the competitor from a threat into the paper's
motivating construct.

---

## 5. Concrete changes this analysis forces

- [x] Add a threat code for their vector (iv), the **reverse attack pathway** — it exists in their
      taxonomy and has no counterpart in ours.
- [x] Add a **`lifecycle_stage`** field, so we can answer their gap #1 (lifecycle-aware security)
      rather than only their gap #2 (empirical validation). One column, large payoff.
- [ ] Map our threat vocabulary onto their five vectors as a table in §4.
- [ ] Cite them in §1 and §2 and state the delta explicitly — do not let a reviewer find them.
- [ ] In §7, note that our retrieval included attack-side operators (`attack`, `adversarial`,
      `intrusion`, `breach`) whereas theirs did not, and that this is a design difference, not an
      accident.

---

## 6. What we still cannot know

We have their **synthesis**, not their **included-study list** — Table 3 names only ~10 of the 20
studies, several only by first author and year. We therefore **cannot quantify corpus overlap** until
their reference list is parsed against ours. Low priority: with N=20 across manufacturing, healthcare
and IIoT, the overlap with a grid corpus is likely 1–3 studies.

Residual risk is now **low**. Their contribution is theory; ours is measurement. The realistic worst
case is a reviewer saying "this extends Habeeb et al. to a new domain" — which is a fair description
of a legitimate paper, not a rejection.
