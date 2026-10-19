#!/usr/bin/env python3
"""Inter-coder agreement for the 20-paper reliability sample.

Cohen's kappa for nominal fields. Multi-label fields (threat_models_named,
ml_family) are scored by exact-set match plus mean Jaccard. Where a field has no
variance in one or both coders (kappa's chance term = 1), kappa is undefined and
only the raw agreement is reported — that is the honest number for the sparse
AI-threat fields, not a 0 or a 1.
"""
import csv
import os
from itertools import combinations

AN = "/mnt/drive2/newpaper/analysis/reliability"

# field -> kind
NOMINAL = [
    "stance", "stance_confidence", "dt_type", "grid_domain", "twin_role",
    "lifecycle_stage", "ml_role", "ai_threat_overall", "eval_method", "maturity",
]
BINARY = [
    "security_primary", "attack_surface_named", "adversary_adaptive",
    "threat_model_explicit", "ml_used", "ai_adv_ml", "ai_evasion", "ai_poisoning",
    "ai_llm", "ai_agentic", "metrics_reported", "baseline_compared",
    "limitations_stated", "code_available", "data_available",
]
SETS = ["threat_models_named", "ml_family"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def asint(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def kappa(pairs):
    n = len(pairs)
    cats = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    po = sum(1 for a, b in pairs if a == b) / n
    pe = sum((sum(1 for a, _ in pairs if a == c) / n) *
             (sum(1 for _, b in pairs if b == c) / n) for c in cats)
    if pe >= 1:
        return None, po
    return (po - pe) / (1 - pe), po


def band(k):
    if k is None:
        return "n/a"
    for t, s in ((.81, "almost perfect"), (.61, "substantial"), (.41, "moderate"),
                 (.21, "fair"), (0, "slight")):
        if k >= t:
            return s
    return "poor"


def setscore(a, b):
    A = {x for x in a.split(";") if x}
    B = {x for x in b.split(";") if x}
    if not A and not B:
        return 1.0, 1.0
    j = len(A & B) / len(A | B) if (A | B) else 1.0
    return (1.0 if A == B else 0.0), j


def main():
    # coder1_sheet.csv is the blank template; C1's codes are in coder1_codes.csv.
    c1 = load("/mnt/drive2/newpaper/analysis/coder1_codes.csv")
    c2 = load(os.path.join(AN, "coder2_sheet.csv"))
    ids = sorted(set(c1) & set(c2), key=int)
    assert len(ids) == 20, f"expected 20 shared ids, got {len(ids)}"

    print(f"reliability sample: {len(ids)} papers, coders C1 vs C2\n")
    print(f"{'field':24s} {'n':>3} {'%agree':>7} {'kappa':>7} {'maj%':>5}  interpretation")
    print("-" * 80)
    rows = []
    for f in NOMINAL + BINARY:
        pairs = [(c1[i][f].strip().lower(), c2[i][f].strip().lower()) for i in ids]
        k, po = kappa(pairs)
        from collections import Counter
        maj = max(Counter(a for a, _ in pairs).values()) / len(pairs)
        ks = "n/a" if k is None else f"{k:.2f}"
        note = band(k) if k is not None else "undefined (zero prevalence / no variance)"
        if k is not None and maj >= 0.9:
            note += " [DEGENERATE: one category >=90%]"
        print(f"{f:24s} {len(pairs):>3} {po*100:>6.0f}% {ks:>7} {maj*100:>4.0f}%  {note}")
        rows.append((f, len(pairs), po, k))

    for f in SETS:
        exact = [setscore(c1[i][f], c2[i][f]) for i in ids]
        em = sum(1 for e, _ in exact if e) / len(ids)
        mj = sum(j for _, j in exact) / len(ids)
        print(f"{f:24s} {len(ids):>3} {em*100:>6.0f}% {'—':>7}  exact-set "
              f"(mean Jaccard {mj:.2f})")
        rows.append((f, len(ids), em, None))

    # threat_count: integer agreement + mean abs difference (ignore blanks)
    pairs = [(asint(c1[i]["threat_count"]), asint(c2[i]["threat_count"])) for i in ids]
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    ae = sum(1 for x, y in pairs if x == y) / len(pairs)
    mad = sum(abs(x - y) for x, y in pairs) / len(pairs)
    print(f"{'threat_count':24s} {len(pairs):>3} {ae*100:>6.0f}% {'—':>7}  "
          f"(mean |diff| {mad:.2f})")

    print("\nNote: kappa is reported only where the chance term is defined; for a field "
          "constant across both coders, only % agreement is meaningful.")


if __name__ == "__main__":
    main()
