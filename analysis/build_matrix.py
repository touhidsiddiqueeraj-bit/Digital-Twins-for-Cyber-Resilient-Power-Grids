#!/usr/bin/env python3
"""Build the extraction matrix and the inter-rater reliability sample.

Sources
  downloads_manifest.csv                     bibliographic + stance seed
  analysis/doi_verification_all.csv          DOI verification outcome
  digital_twin_grid_cybersecurity_papers.csv abstracts (for coder sheets)

Outputs
  analysis/extraction_matrix.csv             100 rows, coding columns empty
  analysis/reliability/sample20.csv          the stratified reliability sample
  analysis/reliability/coder1_sheet.csv      blank coding sheet (coder 1)
  analysis/reliability/coder2_sheet.csv      blank coding sheet (coder 2)
"""
import csv
import os
import random
from collections import Counter, defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AN = os.path.join(ROOT, "analysis")
REL = os.path.join(AN, "reliability")
SEED = 20261016
N_SAMPLE = 20

STANCE_MAP = {
    "defensive": "defensive",
    "review/survey": "review",
    "enabling (security secondary)": "enabling",
    "adversarial": "adversarial",
    "bridge (attack+defence)": "bridge",
}

VENUE_TYPE_MAP = {
    "article": "journal", "review": "journal", "conference-paper": "conference",
    "dissertation": "thesis", "book-chapter": "book_chapter", "book": "book_chapter",
    "preprint": "preprint", "report": "report",
}

CODING_COLS = [
    # abstract-level
    "stance", "stance_confidence", "security_primary",
    # classification (full text)
    "dt_type", "grid_domain", "twin_role", "attack_surface_named", "lifecycle_stage",
    # threat model (full text)
    "threat_models_named", "threat_count", "adversary_adaptive", "threat_model_explicit",
    # AI/ML (full text)
    "ml_used", "ml_role", "ml_family",
    # AI-threat engagement (full text)
    "ai_threat_overall", "ai_adv_ml", "ai_evasion", "ai_poisoning", "ai_llm", "ai_agentic",
    "ai_threat_note",
    # evaluation + rigour (full text)
    "eval_method", "testbed_or_dataset", "metrics_reported", "baseline_compared",
    "maturity", "limitations_stated", "code_available", "data_available",
    # bookkeeping
    "coder", "adjudicated", "notes",
]

META_COLS = [
    "id", "title", "authors", "year", "venue", "venue_type", "publisher",
    "doi", "doi_status", "cited_by", "fulltext", "local_path",
]

SHEET_COLS = ["id", "title", "authors", "year", "venue", "doi", "fulltext",
              "local_path", "abstract"] + CODING_COLS


def venue_type(row):
    t = (row.get("type") or "").strip()
    if t in VENUE_TYPE_MAP:
        return VENUE_TYPE_MAP[t]
    v = (row.get("venue_clean") or "").lower()
    if any(k in v for k in ("journal", "transactions", "letters", "review", "systems")):
        return "journal"
    return "report"


def largest_remainder(counts, total):
    """Apportion `total` across strata in proportion to `counts`."""
    n = sum(counts.values())
    if n == 0:
        return {}
    exact = {k: counts[k] * total / n for k in counts}
    base = {k: int(v) for k, v in exact.items()}
    short = total - sum(base.values())
    for k in sorted(exact, key=lambda k: (-(exact[k] - base[k]), k))[:short]:
        base[k] += 1
    # never allocate more than the stratum holds
    for k in base:
        base[k] = min(base[k], counts[k])
    return base


def main():
    os.makedirs(REL, exist_ok=True)
    man = list(csv.DictReader(open(os.path.join(ROOT, "downloads_manifest.csv"), encoding="utf-8")))
    abstracts = {r["doi"].lower().strip(): r.get("abstract", "")
                 for r in csv.DictReader(open(os.path.join(ROOT, "digital_twin_grid_cybersecurity_papers.csv"),
                                              encoding="utf-8"))}
    verif = {}
    vpath = os.path.join(AN, "doi_verification_all.csv")
    if os.path.exists(vpath):
        verif = {x["id"]: x["status"] for x in csv.DictReader(open(vpath, encoding="utf-8"))}

    matrix = []
    for i, r in enumerate(man, 1):
        doi = (r["doi_clean"] or "").strip()
        row = {
            "id": i,
            "title": r["title"],
            "authors": r["authors"],
            "year": r["year"],
            "venue": r["venue_clean"],
            "venue_type": venue_type(r),
            "publisher": r["publisher"],
            "doi": doi,
            "doi_status": verif.get(str(i), "unverified"),
            "cited_by": r["cited_by"],
            "fulltext": "yes" if r["local_path"] else "no",
            "local_path": r["local_path"],
        }
        # seed the stance C1 already assigned, mapped onto the codebook vocabulary
        raw = (r["stance"] or "").strip().lower()
        row["stance_seed_from_openalex_screening"] = STANCE_MAP.get(raw, "")
        for c in CODING_COLS:
            row.setdefault(c, "")
        matrix.append(row)

    cols = META_COLS + ["stance_seed_from_openalex_screening"] + CODING_COLS
    with open(os.path.join(AN, "extraction_matrix.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(matrix)

    # ---- reliability sample: stratified by stance, drawn only from full texts ----
    pool = [m for m in matrix if m["fulltext"] == "yes"]
    counts = Counter(m["stance_seed_from_openalex_screening"] for m in pool)
    alloc = largest_remainder(counts, N_SAMPLE)
    rng = random.Random(SEED)
    sample = []
    for stance, k in sorted(alloc.items()):
        rows = sorted([m for m in pool if m["stance_seed_from_openalex_screening"] == stance],
                      key=lambda x: x["id"])
        sample += rng.sample(rows, k)
    sample.sort(key=lambda x: x["id"])

    with open(os.path.join(REL, "sample20.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=META_COLS + ["stance_seed_from_openalex_screening"],
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(sample)

    # ---- coder sheets: identical blanks, so the exercise is symmetric ----
    for coder in ("coder1", "coder2"):
        out = []
        for m in sample:
            s = {k: m.get(k, "") for k in SHEET_COLS}
            s["abstract"] = abstracts.get((m["doi"] or "").lower(), "")
            for c in CODING_COLS:
                s[c] = ""
            out.append(s)
        with open(os.path.join(REL, f"{coder}_sheet.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=SHEET_COLS, extrasaction="ignore")
            w.writeheader()
            w.writerows(out)

    # ---- report ----
    print("extraction_matrix.csv :", len(matrix), "rows,", len(cols), "columns")
    print("  full text  :", sum(1 for m in matrix if m["fulltext"] == "yes"))
    print("  abstract   :", sum(1 for m in matrix if m["fulltext"] == "no"))
    print("  doi_status :", dict(Counter(m["doi_status"] for m in matrix)))
    print("  venue_type :", dict(Counter(m["venue_type"] for m in matrix)))
    print()
    print("reliability sample: ", len(sample), "of", len(pool), "full-text records",
          f"({100 * len(sample) / len(pool):.0f}%)")
    print("  stratum sizes in pool :", dict(counts))
    print("  allocation            :", dict(alloc))
    print("  achieved              :",
          dict(Counter(m["stance_seed_from_openalex_screening"] for m in sample)))
    print()
    print("  sample ids:", [m["id"] for m in sample])


if __name__ == "__main__":
    main()
