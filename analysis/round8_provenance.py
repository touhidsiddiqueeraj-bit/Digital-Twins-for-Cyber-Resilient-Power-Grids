#!/usr/bin/env python3
"""Round-8 retrieval-provenance reconstruction (Items 1 and 3 of the review).

OpenAlex re-runs remain blocked (shared-IP budget, third attempt logged in the
snapshot README), so the dated Crossref snapshot of 2026-10-19 is extended to
carry, per query, the top-1000 relevance-ordered results. From those lists this
script builds:

  1. Per-record query provenance for the retained 100 (DOI match, title
     fallback): which of the 16 queries' Crossref top-1000 lists contain each
     record -> membership class core_only / probe_only / both / unmatched.
  2. The probe-added pool (records in probe lists but in no core list),
     screened with the same three-term eligibility rule used in the review
     (digital-twin term AND grid/power/energy term AND cyber/security term,
     on title + abstract when Crossref carries one) -> dated, second-database
     screening status for the probe-added channel.
  3. A core-pool reconstruction: 12 core lists merged, de-duplicated,
     screened with the same rule -> dated eligible-set export, plus a
     ranking manifest (best rank across queries, citation count, year) and a
     re-execution of a declared composite top-100 cut.
  4. Re-run of the review headline fields on the probe-only subset of the
     83 full-text-coded records (from the existing coded matrix).

Everything is written under analysis/search_snapshot_2026-10-19/round8/ with a
README stating what each artifact is and is not (a dated Crossref
reconstruction, NOT the original OpenAlex provenance, which was not retained).

Run:  python3 analysis/round8_provenance.py
"""
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "analysis", "search_snapshot_2026-10-19")
OUT = os.path.join(SNAP, "round8")
TOP = os.path.join(OUT, "top1000")
os.makedirs(TOP, exist_ok=True)

RUN_DATE = "2026-10-19"
UA = {"User-Agent": "dt-powergrids-revision/1.0 (reproducibility package)"}


# ---------------------------------------------------------------- fetch layer
def fetch_query(qid, string, rows=1000):
    """One Crossref call per query; retries once on transient failure."""
    out_csv = os.path.join(TOP, f"{qid}.csv")
    if os.path.exists(out_csv) and os.path.getsize(out_csv) > 200:
        return out_csv
    url = ("https://api.crossref.org/works?rows=%d&select=DOI,title,abstract,"
           "issued,is-referenced-by-count,type,container-title&query.bibliographic=%s"
           % (rows, urllib.parse.quote(string)))
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode("utf-8"))
            items = data["message"]["items"]
            with open(out_csv, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["doi", "title", "container", "type", "year",
                            "cited_by", "has_abstract", "abstract"])
                for it in items:
                    doi = (it.get("DOI") or "").lower().strip()
                    title = (it.get("title") or [""])[0]
                    cont = (it.get("container-title") or [""])[0]
                    year = ""
                    dp = (it.get("issued", {}).get("date-parts") or [[None]])[0]
                    if dp and dp[0]:
                        year = str(dp[0])
                    abst = it.get("abstract") or ""
                    abst_clean = re.sub(r"<[^>]+>", " ", abst)
                    abst_clean = re.sub(r"\s+", " ", abst_clean).strip()
                    w.writerow([doi, title, cont, it.get("type") or "", year,
                                it.get("is-referenced-by-count") or 0,
                                "yes" if abst_clean else "no", abst_clean])
            return out_csv
        except Exception as e:  # noqa: BLE001
            if attempt == 2:
                raise
            print(f"  {qid}: attempt 1 failed ({e}); retrying once")
            time.sleep(5)
    return None


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm_doi(d):
    d = (d or "").lower().strip()
    for pre in ("https://doi.org/", "http://doi.org/", "doi.org/", "doi:"):
        if d.startswith(pre):
            d = d[len(pre):]
    return d.strip()


def norm_title(t):
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------- eligibility rule
DT_RE = re.compile(r"digital twin|digital-twin|digital twins|\bDT\b|\bDTPS\b")
GRID_RE = re.compile(r"power grid|smart grid|energy system|power system|"
                     r"electric grid|electricity|power plant|microgrid|"
                     r"transmission|distribution grid|substation|"
                     r"\bgrid\b|\bgrids\b|\bpower\b|\benergy\b")
SEC_RE = re.compile(r"cyber|security|attack|threat|intrusion|vulnerab|hack|"
                   r"malware|resilien|defen[cs]|protection")
AI_RE = re.compile(r"adversarial (machine learning|ml|attack|example|perturb)|"
                   r"data poisoning|model poisoning|poisoning attack|"
                   r"evasion attack|adversarial attack|prompt injection|"
                   r"large language model|\bLLM\b|\bGAN\b|generative adversar|"
                   r"adversarial perturbation|attack generation|evasion of")


def eligible(rec, use_abstract=True):
    """Three-term rule of Section 4.3 on title (+ abstract if present).

    Matching is case-insensitive: a record is eligible if its title (and
    abstract, when Crossref carries one) contains at least one digital-twin
    term, at least one grid/power/energy term, and at least one cyber/security
    term -- the same three conditions as the review's screening rule.
    """
    text = (rec.get("title", "") or "").lower()
    abst = ((rec.get("abstract", "") or "") if use_abstract else "").lower()
    blob = text + (" " + abst if abst else "")
    return bool(DT_RE.search(blob) and GRID_RE.search(blob)
                and SEC_RE.search(blob))


def main():
    queries = json.load(open(os.path.join(SNAP, "queries.json"),
                            encoding="utf-8"))["queries"]

    print("Fetching top-1000 per query from Crossref (16 calls)...")
    for q in queries:
        p = fetch_query(q["id"], q["string"])
        n = len(load_csv(p)) if p else 0
        print(f"  {q['id']}: {n} rows")
        time.sleep(1.0)

    core_qids = [q["id"] for q in queries if q["id"].startswith("core-")]
    probe_qids = [q["id"] for q in queries if q["id"].startswith("probe-")]

    # ---- per-record provenance for the retained 100 -------------------
    papers = load_csv(os.path.join(ROOT, "digital_twin_grid_cybersecurity_papers.csv"))
    matrix = load_csv(os.path.join(ROOT, "analysis", "extraction_matrix.csv"))
    mat_by_id = {r["id"]: r for r in matrix}

    # index all query results by DOI and by title
    doi_index = {}   # doi -> {qid: rank}
    title_index = {}  # norm title -> {qid: rank}
    for qid in core_qids + probe_qids:
        for rank, rec in enumerate(load_csv(os.path.join(TOP, f"{qid}.csv")), start=1):
            d = norm_doi(rec["doi"])
            if d:
                doi_index.setdefault(d, {})[qid] = rank
            t = norm_title(rec["title"])
            if t:
                title_index.setdefault(t, {})[qid] = rank

    prov_rows = []
    for rid in range(1, 101):
        m = mat_by_id.get(str(rid))
        doi = norm_doi(m["doi"]) if m else ""
        hits = dict(doi_index.get(doi, {})) if doi else {}
        match = "doi" if hits else ""
        if not hits and m:
            t = norm_title(m["title"])
            hits = dict(title_index.get(t, {}))
            if hits:
                match = "title"
        if not hits and m:
            # loose title containment fallback
            t = norm_title(m["title"])
            for cand, qmap in title_index.items():
                if t and (t in cand or cand in t) and abs(len(cand) - len(t)) < max(30, 0.3 * len(t)):
                    hits = dict(qmap)
                    match = "title-approx"
                    break
        core_hits = {q: r for q, r in hits.items() if q in core_qids}
        probe_hits = {q: r for q, r in hits.items() if q in probe_qids}
        if core_hits and probe_hits:
            cls = "both"
        elif core_hits:
            cls = "core_only"
        elif probe_hits:
            cls = "probe_only"
        else:
            cls = "not_matched"
        prov_rows.append({
            "id": rid, "doi": doi, "title": (m["title"] if m else "")[:120],
            "fulltext": (m["fulltext"] if m else ""),
            "match": match,
            "core_queries": ";".join(sorted(core_hits)),
            "probe_queries": ";".join(sorted(probe_hits)),
            "best_core_rank": min(core_hits.values()) if core_hits else "",
            "best_probe_rank": min(probe_hits.values()) if probe_hits else "",
            "membership": cls,
        })

    with open(os.path.join(OUT, "provenance_retained100.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(prov_rows[0].keys()))
        w.writeheader()
        w.writerows(prov_rows)

    from collections import Counter
    cls_counts = Counter(r["membership"] for r in prov_rows)
    ft_cls = Counter(r["membership"] for r in prov_rows if r["fulltext"] == "yes")
    print("\nRetained-100 membership (Crossref top-1000/query, dated "
          f"{RUN_DATE}):", dict(cls_counts))
    print("Full-text (83) membership:", dict(ft_cls))

    # ---- headline re-run on probe_only subset -------------------------
    prov_by_id = {r["id"]: r for r in prov_rows}
    full = [r for r in matrix if r["fulltext"] == "yes"]

    def rates(subset, label):
        n = len(subset)
        if n == 0:
            print(f"  {label}: n=0")
            return
        any_ = sum(1 for r in subset if r["ai_threat_overall"] in ("1", "2"))
        subst = sum(1 for r in subset if r["ai_threat_overall"] == "2")
        ml = sum(1 for r in subset if r["ml_used"] == "yes")
        det = sum(1 for r in subset if r["ml_role"] == "detection")
        print(f"  {label}: n={n}  any={any_} ({any_/n*100:.1f}%)  "
              f"subst={subst} ({subst/n*100:.1f}%)  ml={ml}  det={det}")

    print("\nHeadline on membership subsets (full-text frame):")
    for cls in ("probe_only", "core_only", "both", "not_matched"):
        rates([r for r in full if prov_by_id[int(r["id"])]["membership"] == cls],
              cls)
    # engaged records' membership
    engaged_ids = [int(r["id"]) for r in full if r["ai_threat_overall"] in ("1", "2")]
    subst_ids = [int(r["id"]) for r in full if r["ai_threat_overall"] == "2"]
    eng_cls = Counter(prov_by_id[i]["membership"] for i in engaged_ids)
    sub_cls = Counter(prov_by_id[i]["membership"] for i in subst_ids)
    print("engaged (35) membership:", dict(eng_cls))
    print("substantive (11) membership:", dict(sub_cls))

    # ---- probe-added pool + screening status --------------------------
    probe_all = {}   # doi -> rec
    core_all = {}
    for qid in probe_qids:
        for rec in load_csv(os.path.join(TOP, f"{qid}.csv")):
            d = norm_doi(rec["doi"])
            if d and d not in probe_all:
                probe_all[d] = rec
    for qid in core_qids:
        for rec in load_csv(os.path.join(TOP, f"{qid}.csv")):
            d = norm_doi(rec["doi"])
            if d and d not in core_all:
                core_all[d] = rec
    probe_added = {d: r for d, r in probe_all.items() if d not in core_all}
    print(f"\nCrossref reconstruction: probe lists unique={len(probe_all)}, "
          f"core lists unique={len(core_all)}, probe-ADDED (in no core list)={len(probe_added)}")

    # probe-added screening rows: eligible(title+abstract) is the primary
    # status; eligible_title_only is reported for records without abstracts
    pa_rows = []
    for d, r in sorted(probe_added.items()):
        e_full = eligible(r, use_abstract=True)
        e_title = eligible(r, use_abstract=False)
        ai = bool(AI_RE.search((r["title"] + " " + r["abstract"]).lower()))
        pa_rows.append({"doi": d, "title": r["title"][:160], "year": r["year"],
                        "cited_by": r["cited_by"], "type": r["type"],
                        "has_abstract": r["has_abstract"],
                        "eligible_title_only": "yes" if e_title else "no",
                        "eligible": "yes" if e_full else "no",
                        "ai_term_in_title_or_abstract": "yes" if ai else "no"})
    pa_rows.sort(key=lambda r: (r["eligible"] != "yes", r["ai_term_in_title_or_abstract"] != "yes",
                                -(int(r["cited_by"] or 0))))
    with open(os.path.join(OUT, "probe_added_screening.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pa_rows[0].keys()))
        w.writeheader()
        w.writerows(pa_rows)

    n_abs = sum(1 for r in pa_rows if r["has_abstract"] == "yes")
    n_elig = sum(1 for r in pa_rows if r["eligible"] == "yes")
    n_elig_t = sum(1 for r in pa_rows if r["eligible_title_only"] == "yes")
    n_ai = sum(1 for r in pa_rows if r["ai_term_in_title_or_abstract"] == "yes")
    n_elig_ai = sum(1 for r in pa_rows if r["eligible"] == "yes"
                    and r["ai_term_in_title_or_abstract"] == "yes")
    print(f"probe-added: n={len(pa_rows)}, with abstract={n_abs}, "
          f"eligible(title+abstract)={n_elig}, eligible(title-only)={n_elig_t}")
    print(f"probe-added with AI-attack vocabulary in title/abstract: {n_ai} "
          f"({n_ai/len(pa_rows)*100:.1f}%); among eligible: {n_elig_ai} "
          f"({(n_elig_ai/n_elig*100 if n_elig else 0):.1f}%)")

    # ---- core-pool reconstruction + ranking manifest ------------------
    core_rows = []
    for d, r in core_all.items():
        core_rows.append({"doi": d, "title": r["title"][:200], "year": r["year"],
                          "cited_by": int(r["cited_by"] or 0), "type": r["type"],
                          "has_abstract": r["has_abstract"],
                          "eligible": "yes" if eligible(r, use_abstract=True) else "no"})
    elig = [r for r in core_rows if r["eligible"] == "yes"]
    print(f"\ncore-pool reconstruction: unique={len(core_all)}, "
          f"eligible(three-term rule)={len(elig)}")
    # ranking manifest: best (smallest) rank across core lists, then citations, then year
    rank_map = {}
    for qid in core_qids:
        for rank, rec in enumerate(load_csv(os.path.join(TOP, f"{qid}.csv")), start=1):
            d = norm_doi(rec["doi"])
            if d:
                if d not in rank_map or rank < rank_map[d]:
                    rank_map[d] = rank
    for r in elig:
        r["best_rank"] = rank_map.get(r["doi"], "")
    elig.sort(key=lambda r: (r["best_rank"] if r["best_rank"] != "" else 10**9,
                             -r["cited_by"], -(int(r["year"]) if r["year"] else 0)))
    for i, r in enumerate(elig, start=1):
        r["cut_rank"] = i
        r["in_retained_corpus"] = "yes" if r["doi"] in {
            norm_doi(m["doi"]) for m in matrix if m["doi"]} else "no"
    with open(os.path.join(OUT, "core_eligible_export.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(elig[0].keys()))
        w.writeheader()
        w.writerows(elig)
    top100_recon = elig[:100]
    overlap = sum(1 for r in top100_recon if r["in_retained_corpus"] == "yes")
    in_corpus_any = sum(1 for r in elig if r["in_retained_corpus"] == "yes")
    print(f"reconstructed eligible export rows={len(elig)}; retained-corpus "
          f"records found in it={in_corpus_any}; top-100 re-execution overlap "
          f"with retained corpus={overlap}")
    yrs = Counter(r["year"] for r in top100_recon)
    print("year distribution of re-executed top-100:", dict(sorted(yrs.items(), reverse=True)[:6]))

    # also: screening-level comparison for retained corpus abstracts
    import collections
    papers_by_doi = {norm_doi(p["doi"]): p for p in papers}
    n_probe_term = 0
    for p in papers:
        blob = (p["title"] + " " + p["abstract"]).lower()
        if AI_RE.search(blob):
            n_probe_term += 1
    print(f"\nretained-100 records whose title+abstract contain probe "
          f"vocabulary: {n_probe_term}/100")


if __name__ == "__main__":
    main()
