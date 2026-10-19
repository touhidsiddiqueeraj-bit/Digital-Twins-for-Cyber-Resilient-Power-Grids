#!/usr/bin/env python3
"""Round-8: (a) probe-added screening breakdown by eligibility term;
(b) ranking manifest for the retained 100 (Item 3).

(a) For the dated Crossref reconstruction of the probe-added pool (records in
probe top-1000 lists but no core list), reports which of the three eligibility
terms (digital-twin / grid / security) each record passes in title+abstract.
This decomposes *where* the attack-side literature is lost between retrieval
and eligibility -- the concrete shape of the retrieval bias.

(b) Rebuilds, from the released corpus CSV, the ranking manifest the review's
Selection section describes: per retained record, its OpenAlex relevance score
and citation count as retrieved, its year, and the display-order claim (year
descending, citations descending within year). The manifest makes the
realised corpus's ranking components inspectable even though the composite
weights of the original top-100 cut cannot be recovered.

Outputs (analysis/search_snapshot_2026-10-19/reconstruction/):
  probe_added_term_breakdown.csv  -- per-record dt/grid/security term flags
  retained100_ranking_manifest.csv
"""
import csv
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "analysis", "search_snapshot_2026-10-19", "reconstruction")

DT_RE = re.compile(r"digital[\s-]*twins?")
GRID_RE = re.compile(r"grid|power|energy")
SEC_RE = re.compile(r"cyber|secur|attack|threat|intrusion|vulnerab|hack|"
                    r"malware|resilien|defen[cs]|protection")
AI_RE = re.compile(r"adversarial (machine learning|ml|attack|example|perturb)|"
                   r"data poisoning|model poisoning|poisoning attack|"
                   r"evasion attack|adversarial attack|prompt injection|"
                   r"large language model|\bllm\b|\bgan\b|generative adversar|"
                   r"adversarial perturbation|attack generation|evasion of")


def main():
    pa = list(csv.DictReader(open(os.path.join(OUT, "probe_added_screening.csv"),
                                  encoding="utf-8")))
    top = {}
    import json
    # reload full text from the cached top-1000 lists for term flags
    for qid in ("probe-01", "probe-02", "probe-03", "probe-04"):
        for r in csv.DictReader(open(os.path.join(OUT, "top1000", f"{qid}.csv"),
                                     encoding="utf-8")):
            d = r["doi"].lower().strip()
            if d not in top:
                top[d] = r
    rows = []
    for r in pa:
        d = r["doi"].lower().strip()
        rec = top.get(d, {})
        text = (rec.get("title", "") + " " + rec.get("abstract", "")).lower()
        rows.append({
            "doi": d, "title": rec.get("title", "")[:150],
            "has_abstract": rec.get("has_abstract", ""),
            "dt_term": "yes" if DT_RE.search(text) else "no",
            "grid_term": "yes" if GRID_RE.search(text) else "no",
            "sec_term": "yes" if SEC_RE.search(text) else "no",
            "ai_vocab": "yes" if AI_RE.search(text) else "no",
        })
    with open(os.path.join(OUT, "probe_added_term_breakdown.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    flags = Counter()
    for r in rows:
        k = (r["dt_term"], r["grid_term"], r["sec_term"])
        flags[k] += 1
    print(f"probe-added pool: n={n}")
    for k, v in sorted(flags.items(), key=lambda kv: -kv[1]):
        print(f"  dt={k[0]:3s} grid={k[1]:3s} sec={k[2]:3s} -> {v}")
    ai_rows = [r for r in rows if r["ai_vocab"] == "yes"]
    print(f"\nprobe-added with AI-attack vocabulary: {len(ai_rows)}")
    ai_flags = Counter((r["dt_term"], r["grid_term"], r["sec_term"]) for r in ai_rows)
    for k, v in sorted(ai_flags.items(), key=lambda kv: -kv[1]):
        print(f"  dt={k[0]:3s} grid={k[1]:3s} sec={k[2]:3s} -> {v}")
    ai_dt = sum(1 for r in ai_rows if r["dt_term"] == "yes")
    ai_dt_sec = sum(1 for r in ai_rows if r["dt_term"] == "yes" and r["sec_term"] == "yes")
    ai_dt_grid = sum(1 for r in ai_rows if r["dt_term"] == "yes" and r["grid_term"] == "yes")
    ai_all = sum(1 for r in ai_rows if r["dt_term"] == "yes" and r["grid_term"] == "yes"
                 and r["sec_term"] == "yes")
    print(f"  of those: with DT term={ai_dt}, DT+grid={ai_dt_grid}, "
          f"DT+sec={ai_dt_sec}, all three={ai_all}")

    # ---- retained-100 ranking manifest --------------------------------
    papers = list(csv.DictReader(open(
        os.path.join(ROOT, "digital_twin_grid_cybersecurity_papers.csv"),
        encoding="utf-8")))
    matrix = {r["id"]: r for r in csv.DictReader(open(
        os.path.join(ROOT, "analysis", "extraction_matrix.csv"), encoding="utf-8"))}
    man = []
    for i, p in enumerate(papers, start=1):
        m = matrix[str(i)]
        man.append({
            "id": i, "year": p["year"], "cited_by_at_retrieval": p["cited_by"],
            "openalex_relevance": p["relevance"], "venue_type": m["venue_type"],
            "stance": m["stance"], "fulltext": m["fulltext"],
            "ai_threat_overall": m["ai_threat_overall"],
        })
    with open(os.path.join(OUT, "retained100_ranking_manifest.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(man[0].keys()))
        w.writeheader()
        w.writerows(man)
    # verify display-order claim: year descending, citations desc within year
    ok = True
    prev_year, prev_cit = None, None
    for r in man:
        y, c = int(r["year"]), int(r["cited_by_at_retrieval"] or 0)
        if prev_year is not None:
            if y > prev_year:
                ok = False
                print(f"  display-order violation at id {r['id']}: year {y} > {prev_year}")
            elif y == prev_year and c > prev_cit:
                ok = False
                print(f"  display-order violation at id {r['id']}: citations {c} > {prev_cit} within {y}")
        prev_year, prev_cit = y, c
    print(f"\nranking manifest: n={len(man)}; display-order claim "
          f"(year desc, citations desc within year) holds: {ok}")
    n_zero = sum(1 for r in man if int(r["cited_by_at_retrieval"] or 0) == 0)
    print(f"zero-citation records at retrieval: {n_zero}/100")


if __name__ == "__main__":
    main()
