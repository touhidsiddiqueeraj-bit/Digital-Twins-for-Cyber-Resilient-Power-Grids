#!/usr/bin/env python3
"""Round-8: independent (AI-instrument) reliability readback statistics.

Consumes analysis/reliability/round8_ai_readback_codes.csv (a full census of
the 83 full-text records, coded by a non-author automated reader from the
released evidence dump) and computes:

  1. Census agreement with coder 1's adjudicated ai_threat_overall:
     percentage agreement, Cohen's kappa and PABAK on (a) the three-level
     scale, (b) the any-engagement collapse (0 vs >=1), (c) the substantive
     collapse (0/1 vs 2).
  2. Three-way comparison on the 20-record reliability sample (coder 1 vs
     coder 2 vs the round-8 reader).
  3. Negative-census miss-rate: suspected score-1 and score-2 misses among
     the 48 zero-coded records, Wilson 95% CI, and the propagated headline.
  4. Direction split (Item 6): per-record direction (on / with / both /
     unclear) for every engaged record, with counts overall, by tier, and
     per AI-threat vector.
"""
import csv
import math
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AN = os.path.join(ROOT, "analysis")


def kappa_collapse(pairs):
    """Cohen's kappa for binary lists of (r1, r2)."""
    n = len(pairs)
    cats = sorted({v for p in pairs for v in p})
    if len(cats) < 2:
        return None
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for c in cats:
        m1 = sum(1 for a, _ in pairs if a == c) / n
        m2 = sum(1 for _, b in pairs if b == c) / n
        pe += m1 * m2
    if pe == 1.0:
        return None
    return (po - pe) / (1 - pe)


def kappa_multiclass(rows_a, rows_b):
    n = len(rows_a)
    cats = sorted(set(rows_a) | set(rows_b))
    po = sum(1 for a, b in zip(rows_a, rows_b) if a == b) / n
    pe = 0.0
    for c in cats:
        pe += (rows_a.count(c) / n) * (rows_b.count(c) / n)
    return po, pe, (po - pe) / (1 - pe) if pe < 1 else None


def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0, 0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, (c - h) / d, (c + h) / d)


def main():
    matrix = {r["id"]: r for r in csv.DictReader(
        open(os.path.join(AN, "extraction_matrix.csv"), encoding="utf-8"))}
    mine = {r["id"]: r for r in csv.DictReader(
        open(os.path.join(AN, "reliability", "round8_ai_readback_codes.csv"),
             encoding="utf-8"))}
    full_ids = sorted([rid for rid, r in matrix.items()
                       if r["fulltext"] == "yes"], key=int)
    assert len(full_ids) == len(mine) == 83, (len(full_ids), len(mine))
    assert set(full_ids) == set(mine)

    c1 = [matrix[r]["ai_threat_overall"] for r in full_ids]
    r8 = [mine[r]["my_ai_threat_overall"] for r in full_ids]

    print("=== 1. Census agreement (n=83), round-8 reader vs coder 1 ===")
    po, pe, k3 = kappa_multiclass(c1, r8)
    print(f"three-level: agree={sum(1 for a,b in zip(c1,r8) if a==b)}/83 "
          f"({po*100:.1f}%), kappa={k3:.2f}")
    anypairs = [(0 if a == '0' else 1, 0 if b == '0' else 1)
                for a, b in zip(c1, r8)]
    ka = kappa_collapse(anypairs)
    pany = sum(1 for a, _ in anypairs if a == 1) / 83 * 100
    print(f"any-collapse: agree={sum(1 for a,b in anypairs if a==b)}/83 "
          f"({sum(1 for a,b in anypairs if a==b)/83*100:.1f}%), kappa={ka:.2f}, "
          f"PABAK={2*sum(1 for a,b in anypairs if a==b)/83-1:.2f}")
    subpairs = [(0 if a == '2' else 1, 0 if b == '2' else 1)
                for a, b in zip(c1, r8)]
    ks = kappa_collapse(subpairs)
    print(f"substantive-collapse: agree={sum(1 for a,b in subpairs if a==b)}/83, "
          f"kappa={ks:.2f}")
    print(f"coder1 marginals: 0={c1.count('0')}, 1={c1.count('1')}, 2={c1.count('2')}")
    print(f"round8 marginals: 0={r8.count('0')}, 1={r8.count('1')}, 2={r8.count('2')}")
    dis = [(rid, a, b) for rid, a, b in zip(full_ids, c1, r8) if a != b]
    print(f"disagreements ({len(dis)}):", [(f'R{d[0]}', f'c1={d[1]}', f'r8={d[2]}') for d in dis])

    print("\n=== 2. Three-way comparison on the 20-record sample ===")
    c2 = {r["id"]: r["ai_threat_overall"] for r in csv.DictReader(
        open(os.path.join(AN, "reliability", "coder2_sheet.csv"), encoding="utf-8"))}
    sample_ids = sorted(c2, key=int)
    for name, codes in (("coder1", c1), ("round8", r8)):
        idx = [full_ids.index(s) for s in sample_ids]
        pairs = [(0 if codes[i] == '0' else 1,
                  0 if c2[s] == '0' else 1) for s, i in zip(sample_ids, idx)]
        kk = kappa_collapse(pairs)
        ag = sum(1 for a, b in pairs if a == b)
        print(f"{name} vs coder2 (any-collapse): agree={ag}/20, kappa="
              f"{kk if kk is None else round(kk, 2)}")

    print("\n=== 3. Negative-census miss-rate (48 zero-coded records) ===")
    neg_ids = [rid for rid in full_ids if matrix[rid]["ai_threat_overall"] == "0"]
    miss1 = [rid for rid in neg_ids if mine[rid]["my_ai_threat_overall"] == "1"]
    miss2 = [rid for rid in neg_ids if mine[rid]["my_ai_threat_overall"] == "2"]
    p, lo, hi = wilson(len(miss1) + len(miss2), len(neg_ids))
    print(f"suspected score-1 misses: {[f'R{i}' for i in miss1]}")
    print(f"suspected score-2 misses: {[f'R{i}' for i in miss2]}")
    print(f"miss-rate = {len(miss1)+len(miss2)}/{len(neg_ids)} = {p*100:.1f}% "
          f"(Wilson 95% CI {lo*100:.1f}%-{hi*100:.1f}%)")
    k = len(miss1) + len(miss2)
    print(f"propagated headline: 35 -> {35+k} of 83 ({(35+k)/83*100:.1f}%)")
    fl = [f"R{rid}" for rid in full_ids
          if mine[rid].get("flag") in ("borderline", "disagreement")]
    print(f"flagged records: {fl}")

    print("\n=== 4. Direction split (Item 6, all engaged records) ===")
    engaged = [rid for rid in full_ids if matrix[rid]["ai_threat_overall"] in ("1", "2")]
    dir_c1 = Counter(mine[rid]["my_direction"] for rid in engaged)
    print(f"coder-1-engaged (n={len(engaged)}) direction: {dict(dir_c1)}")
    sub = [rid for rid in full_ids if matrix[rid]["ai_threat_overall"] == "2"]
    dsub = Counter(mine[rid]["my_direction"] for rid in sub)
    print(f"substantive (n={len(sub)}) direction: {dict(dsub)}")
    # per-vector direction
    vecs = [("ai_adv_ml", "adversarial ML"), ("ai_poisoning", "poisoning"),
            ("ai_evasion", "evasion"), ("ai_llm", "LLM"),
            ("ai_agentic", "agentic")]
    print("per-vector engagement x direction (rows = ai_* >= 1):")
    for fld, label in vecs:
        ids = [rid for rid in full_ids if matrix[rid][fld] in ("1", "2")]
        d = Counter(mine[rid]["my_direction"] for rid in ids)
        print(f"  {label:15s} n={len(ids):2d}  {dict(d)}")
    # any-level engaged by my direction including my two extra records
    print("\nmy-engaged (n=%d) direction: " % sum(1 for r in r8 if r != '0'),
          dict(Counter(mine[rid]["my_direction"] for rid in full_ids
                       if mine[rid]["my_ai_threat_overall"] != "0")))

    # export the joined direction field for release
    out = []
    for rid in full_ids:
        m, y = matrix[rid], mine[rid]
        out.append({
            "id": rid,
            "coder1_ai_threat_overall": m["ai_threat_overall"],
            "round8_ai_threat_overall": y["my_ai_threat_overall"],
            "round8_direction": y["my_direction"] if m["ai_threat_overall"] != "0"
                                else "",
            "round8_flag": y["flag"],
            "round8_basis": y["basis"],
        })
    with open(os.path.join(AN, "reliability", "round8_readback_joined.csv"),
              "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print("\nwrote analysis/reliability/round8_readback_joined.csv")


if __name__ == "__main__":
    main()
