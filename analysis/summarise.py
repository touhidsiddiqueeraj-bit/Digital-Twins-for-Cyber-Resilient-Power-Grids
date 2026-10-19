#!/usr/bin/env python3
"""Derive every number the paper reports, from extraction_matrix.csv alone.

No number in the manuscript should come from anywhere else. Re-run after any
coding change.
"""
import csv
import collections
import os

AN = os.path.join(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(AN, "extraction_matrix.csv"), encoding="utf-8")))
ft = [r for r in rows if r["fulltext"] == "yes"]
ab = [r for r in rows if r["fulltext"] != "yes"]
AI = ["ai_threat_overall", "ai_adv_ml", "ai_evasion", "ai_poisoning", "ai_llm", "ai_agentic"]
LABEL = {"ai_threat_overall": "any AI-enabled threat", "ai_adv_ml": "adversarial ML",
         "ai_evasion": "ML evasion", "ai_poisoning": "data/model poisoning",
         "ai_llm": "LLM-specific threats", "ai_agentic": "agentic attack automation"}


def dist(rr, f):
    return dict(sorted(collections.Counter(r[f] for r in rr).items()))


def top(rr, f, n=12):
    c = collections.Counter()
    for r in rr:
        for t in [x for x in r[f].split(";") if x]:
            c[t] += 1
    return c.most_common(n)


out = []
w = out.append
w("# Results — derived from extraction_matrix.csv")
w("")
w(f"Corpus: **{len(rows)}** records; full text **{len(ft)}**, abstract-only **{len(ab)}**.")
w("")
w("## Headline: engagement with AI-enabled threats")
w("")
w("Full-text records only (n=%d). Scale 0 = not addressed, 1 = mentioned/peripheral, 2 = substantive." % len(ft))
w("")
w("| Vector | 0 | 1 | 2 | any (>0) | any % |")
w("|---|---|---|---|---|---|")
for f in AI:
    d = collections.Counter(r[f] for r in ft)
    any_n = d.get("1", 0) + d.get("2", 0)
    w(f"| {LABEL[f]} | {d.get('0',0)} | {d.get('1',0)} | {d.get('2',0)} | {any_n} | {100*any_n/len(ft):.1f}% |")
w("")
d = collections.Counter(r["ai_threat_overall"] for r in ft)
w(f"- Papers engaging **any** AI-enabled threat at all (score ≥1): **{d.get('1',0)+d.get('2',0)}/{len(ft)} = {100*(d.get('1',0)+d.get('2',0))/len(ft):.1f}%**")
w(f"- Papers engaging **substantively** (score 2): **{d.get('2',0)}/{len(ft)} = {100*d.get('2',0)/len(ft):.1f}%**")
w(f"- Papers with **no** engagement (score 0): **{d.get('0',0)}/{len(ft)} = {100*d.get('0',0)/len(ft):.1f}%**")
w("")
w("Abstract-only records (n=%d) cannot be coded on these fields; the 17 excluded records are" % len(ab))
w("reported as a limitation. The abstract-level screening figure quoted in earlier drafts")
w("(24/469 = 5.1%) came from an unpreserved scan; treat it as an unreproducible working")
w("number, not evidence (see SEARCH_PROVENANCE.md).")
w("")
w(f"- Non-grid rows flagged in notes (fraud, vehicle and generic-ICS cases): "
  f"{sum(1 for r in rows if 'boundary' in r['notes'].lower() or 'corpus membership' in r['notes'].lower())}")
w("")
w("### Coder 1 stance vs the OpenAlex screening seed")
w("")
w("The seed came from title/abstract screening; the coder-1 column is a read of the paper. A large")
w("shift here is a finding about screening, not a coding error, and must be reported.")
w("")
w("| Stance | seed (screening) | coder 1 |")
w("|---|---|---|")
for k in ["adversarial", "defensive", "bridge", "review", "enabling"]:
    w(f"| {k} | {sum(1 for r in rows if r['stance_seed_from_openalex_screening'].startswith(k))} | "
      f"{sum(1 for r in rows if r['stance']==k)} |")
w("")

w("## Stance")
w("")
w("| Stance | all 100 | full text | abstract-only |")
w("|---|---|---|---|")
for k in ["adversarial", "defensive", "bridge", "review", "enabling"]:
    w(f"| {k} | {sum(1 for r in rows if r['stance']==k)} | {sum(1 for r in ft if r['stance']==k)} | {sum(1 for r in ab if r['stance']==k)} |")
w("")
w(f"- security_primary = yes: **{sum(1 for r in rows if r['security_primary']=='yes')}/100**")
w(f"- stance_confidence low (escalate to adjudication): {[r['id'] for r in rows if r['stance_confidence']=='low']}")
w("")

w("## The dual-role question (twin_role, full text n=%d)" % len(ft))
w("")
for k, v in dist(ft, "twin_role").items():
    w(f"- {k}: {v}")
w("")
w("Twin-as-target or both, i.e. the tension the framing addresses: **%d/%d = %.1f%%**" % (
    sum(1 for r in ft if r["twin_role"] in ("target", "both")), len(ft),
    100 * sum(1 for r in ft if r["twin_role"] in ("target", "both")) / len(ft)))
w("")

w("## Lifecycle stage (full text n=%d) — the competitor's first named gap" % len(ft))
w("")
for k, v in dist(ft, "lifecycle_stage").items():
    w(f"- {k}: {v}")
w("")
w("Operation-only share: **%.1f%%**; design or commissioning addressed at all: **%d** records." % (
    100 * sum(1 for r in ft if r["lifecycle_stage"] == "operation") / len(ft),
    sum(1 for r in ft if r["lifecycle_stage"] in ("design", "commissioning"))))
w("")

w("## Threat vocabulary (full text n=%d)" % len(ft))
w("")
w("| Threat | records naming it |")
w("|---|---|")
for t, n in top(ft, "threat_models_named"):
    w(f"| {t} | {n} |")
w("")
tc = [int(r["threat_count"]) for r in ft]
w(f"- Records naming **no** threat at all: **{sum(1 for x in tc if x==0)}/{len(ft)}**")
w(f"- Mean distinct threats named: **{sum(tc)/len(tc):.2f}**; median {sorted(tc)[len(tc)//2]}; max {max(tc)}")
w("")
w(f"- Adversary modelled as adaptive: **{sum(1 for r in ft if r['adversary_adaptive']=='yes')}/{len(ft)}**")
w(f"- Formal threat model present: **{sum(1 for r in ft if r['threat_model_explicit']=='yes')}/{len(ft)}**")
w("")

w("## Machine learning (full text n=%d)" % len(ft))
w("")
w(f"- Uses ML/AI at all: **{sum(1 for r in ft if r['ml_used']=='yes')}/{len(ft)}**")
w(f"- ml_role: {dict(collections.Counter(r['ml_role'] for r in ft))}")
w("")

w("## Evaluation and rigour (full text n=%d)" % len(ft))
w("")
w(f"- eval_method: {dict(collections.Counter(r['eval_method'] for r in ft))}")
w(f"- maturity: {dict(collections.Counter(r['maturity'] for r in ft))}")
w(f"- metrics_reported=yes: {sum(1 for r in ft if r['metrics_reported']=='yes')}/{len(ft)}")
w(f"- baseline_compared=yes: {sum(1 for r in ft if r['baseline_compared']=='yes')}/{len(ft)}")
w(f"- limitations_stated=yes: {sum(1 for r in ft if r['limitations_stated']=='yes')}/{len(ft)}")
w(f"- code_available=yes: {sum(1 for r in ft if r['code_available']=='yes')}/{len(ft)}")
w(f"- data_available=yes: {sum(1 for r in ft if r['data_available']=='yes')}/{len(ft)}")
w("")

w("## Year")
w("")
for k, v in sorted(collections.Counter(r["year"] for r in rows).items()):
    w(f"- {k}: {v}")
w("")
w(f"2025–2026 share: **{100*sum(1 for r in rows if r['year'] in ('2025','2026'))/len(rows):.1f}%**")
w("")

w("## Grid domain (full text n=%d)" % len(ft))
w("")
for k, v in dist(ft, "grid_domain").items():
    w(f"- {k}: {v}")
w("")

txt = "\n".join(out) + "\n"
open(os.path.join(AN, "RESULTS.md"), "w", encoding="utf-8").write(txt)
print(txt)
