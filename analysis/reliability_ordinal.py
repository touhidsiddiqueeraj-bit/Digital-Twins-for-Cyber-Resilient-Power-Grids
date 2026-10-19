#!/usr/bin/env python3
"""Ordinal reliability statistics: weighted kappa, Gwet's AC1 (all fields), and
family-level threat-vocabulary agreement, computed from the frozen coder sheets.

Usage: python3 analysis/reliability_ordinal.py

Sources:
  - analysis/coder1_codes.csv          (frozen pre-adjudication coder-1 codes, n=100)
  - analysis/reliability/coder2_sheet.csv (blind coder-2 codes, n=20)

Outputs (stdout): the statistics quoted in manuscript Section 5.6 and Table 5
(AC1 column), so every reliability number is reproducible.
"""
import csv
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C1 = {int(r["id"]): r for r in csv.DictReader(open(os.path.join(ROOT, "analysis", "coder1_codes.csv"), encoding="utf-8"))}
C2 = {int(r["id"]): r for r in csv.DictReader(open(os.path.join(ROOT, "analysis", "reliability", "coder2_sheet.csv"), encoding="utf-8"))}
IDS = sorted(C2)
assert len(IDS) == 20, "expected the 20-record blind sample"


def kappa(T):
    n = sum(sum(r) for r in T)
    k = len(T)
    po = sum(T[i][i] for i in range(k)) / n
    pe = sum((sum(T[i]) / n) * (sum(T[j][i] for j in range(k)) / n) for i in range(k))
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def weighted_kappa(T, quad=True):
    n = sum(sum(r) for r in T)
    k = len(T)
    W = [[((i - j) ** 2 / ((k - 1) ** 2)) if quad else (abs(i - j) / (k - 1))
          for j in range(k)] for i in range(k)]
    num = sum(W[i][j] * T[i][j] for i in range(k) for j in range(k)) / n
    rows = [sum(T[i]) / n for i in range(k)]
    cols = [sum(T[j][i] for j in range(k)) / n for i in range(k)]
    den = sum(W[i][j] * rows[i] * cols[j] for i in range(k) for j in range(k))
    return 1 - num / den


def gwet_ac1(T):
    n = sum(sum(r) for r in T)
    k = len(T)
    po = sum(T[i][i] for i in range(k)) / n
    pi = []
    for q in range(k):
        r_q = sum(T[q]) / n
        c_q = sum(T[j][q] for j in range(k)) / n
        pi.append((r_q + c_q) / 2)
    pe = sum(p * (1 - p) for p in pi) / (k - 1)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def table_for(field, cats=None):
    vals = sorted({C1[i][field] for i in IDS} | {C2[i][field] for i in IDS})
    idx = {v: k for k, v in enumerate(vals)}
    T = [[0] * len(vals) for _ in vals]
    for i in IDS:
        T[idx[C1[i][field]]][idx[C2[i][field]]] += 1
    return T


print("== ai_threat_overall (3x3, rows=coder1, cols=coder2) ==")
T = table_for("ai_threat_overall")
for row in T:
    print("  ", row)
print(f"  unweighted kappa      = {kappa(T):.3f}")
print(f"  linear weighted kappa = {weighted_kappa(T, quad=False):.3f}")
print(f"  quadratic w. kappa    = {weighted_kappa(T, quad=True):.3f}")
print(f"  Gwet AC1              = {gwet_ac1(T):.3f}")

# bootstrap CIs (fixed seed for reproducibility)
random.seed(42)
pairs = [(int(C1[i]["ai_threat_overall"]), int(C2[i]["ai_threat_overall"])) for i in IDS]


def boot(fn, B=10000):
    out = []
    for _ in range(B):
        s = [random.choice(pairs) for _ in pairs]
        TT = [[0] * 3 for _ in range(3)]
        for a, b in s:
            TT[a][b] += 1
        out.append(fn(TT))
    out.sort()
    return out[int(0.025 * B)], out[int(0.975 * B)]


for name, fn in (("linear wK", lambda t: weighted_kappa(t, False)),
                 ("quadratic wK", lambda t: weighted_kappa(t, True)),
                 ("AC1", gwet_ac1)):
    lo, hi = boot(fn)
    print(f"  bootstrap 95% CI {name:11s}= [{lo:.3f}, {hi:.3f}]")

print("\n== Gwet AC1, all fields with tables (Table 5 AC1 column) ==")
FIELDS = ["baseline_compared", "twin_role", "ai_poisoning", "threat_model_explicit",
          "metrics_reported", "security_primary", "ml_used", "ml_role", "stance",
          "dt_type", "grid_domain", "ai_adv_ml", "maturity", "ai_threat_overall",
          "ai_evasion", "eval_method", "lifecycle_stage", "attack_surface_named",
          "code_available", "ai_agentic", "ai_llm", "data_available",
          "stance_confidence", "limitations_stated"]
for f in FIELDS:
    print(f"  {f:24s} AC1 = {gwet_ac1(table_for(f)):.2f}")

print("\n== Family-level threat-vocabulary agreement (n=20) ==")
FAMILIES = {
    "interface (mitm/replay/reverse_pathway/false_command)":
        {"mitm", "replay", "reverse_pathway", "false_command"},
    "learned-model (poisoning/evasion/prompt)":
        {"poisoning", "evasion", "prompt"},
    "classical (dos/fdi/malware/physical/insider/supply_chain/hardware/other)":
        {"dos", "fdi", "malware", "physical", "insider", "supply_chain", "hardware", "other"},
}


def toset(s):
    return set(t.strip() for t in (s or "").split(";") if t.strip())


for name, members in FAMILIES.items():
    a = [1 if members & toset(C1[i]["threat_models_named"]) else 0 for i in IDS]
    b = [1 if members & toset(C2[i]["threat_models_named"]) else 0 for i in IDS]
    agree = sum(1 for x, y in zip(a, b) if x == y)
    TT = [[0, 0], [0, 0]]
    for x, y in zip(a, b):
        TT[x][y] += 1
    print(f"  {name}: C1+ {sum(a)}, C2+ {sum(b)}, agree {agree}/20, "
          f"kappa {kappa(TT):.2f}")
