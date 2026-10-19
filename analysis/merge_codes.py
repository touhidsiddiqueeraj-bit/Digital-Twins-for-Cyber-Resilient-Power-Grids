#!/usr/bin/env python3
"""Expand the coder-1 code files into the extraction matrix.

Reads every analysis/codes/part*.txt (delimiter @@), validates the field count,
derives threat_count, sets coder/adjudicated, and writes both
analysis/coder1_codes.csv and the filled analysis/extraction_matrix.csv.

Rows absent from the code files are left blank in the matrix and reported as
remaining, so the coding can proceed in batches.
"""
import csv
import glob
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AN = os.path.join(ROOT, "analysis")

FIELDS = ["id", "stance", "stance_confidence", "security_primary", "dt_type",
          "grid_domain", "twin_role", "attack_surface_named", "lifecycle_stage",
          "threat_models_named", "adversary_adaptive", "threat_model_explicit",
          "ml_used", "ml_role", "ml_family",
          "ai_threat_overall", "ai_adv_ml", "ai_evasion", "ai_poisoning", "ai_llm",
          "ai_agentic", "ai_threat_note",
          "eval_method", "testbed_or_dataset", "metrics_reported", "baseline_compared",
          "maturity", "limitations_stated", "code_available", "data_available",
          "notes"]

CODING_COLS = ["stance", "stance_confidence", "security_primary", "dt_type", "grid_domain",
               "twin_role", "attack_surface_named", "lifecycle_stage",
               "threat_models_named", "threat_count", "adversary_adaptive",
               "threat_model_explicit", "ml_used", "ml_role", "ml_family",
               "ai_threat_overall", "ai_adv_ml", "ai_evasion", "ai_poisoning", "ai_llm",
               "ai_agentic", "ai_threat_note",
               "eval_method", "testbed_or_dataset", "metrics_reported", "baseline_compared",
               "maturity", "limitations_stated", "code_available", "data_available",
               "coder", "adjudicated", "notes"]


def load_codes():
    codes = {}
    bad = []
    for path in sorted(glob.glob(os.path.join(AN, "codes", "part*.txt"))):
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = [p.strip() for p in line.split("@@")]
            if len(parts) != len(FIELDS):
                bad.append(f"{os.path.basename(path)}:{ln} has {len(parts)} fields, expected {len(FIELDS)}")
                continue
            rec = dict(zip(FIELDS, parts))
            codes[int(rec["id"])] = rec
    return codes, bad


def load_overlay():
    """Adjudicated overrides for the reliability sample. Non-empty fields only."""
    path = os.path.join(AN, "codes", "adjudicated.txt")
    out = {}
    if not os.path.exists(path):
        return out
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split("@@")]
        if len(parts) != len(FIELDS):
            print(f"  OVERLAY FIELD-COUNT ERROR: {os.path.basename(path)}:{ln}")
            continue
        rec = dict(zip(FIELDS, parts))
        out[int(rec["id"])] = {k: v for k, v in rec.items() if k != "id" and v != ""}
    return out


def main():
    codes, bad = load_codes()
    for b in bad:
        print("  FIELD-COUNT ERROR:", b)

    overlay = load_overlay()
    for k in overlay:
        if k not in codes:
            print(f"  OVERLAY ERROR: id {k} has no C1 codes")

    mpath = os.path.join(AN, "extraction_matrix.csv")
    rows = list(csv.DictReader(open(mpath, encoding="utf-8")))
    cols = list(rows[0].keys())

    for r in rows:
        rec = codes.get(int(r["id"]))
        if not rec:
            continue
        for c in CODING_COLS:
            if c in ("threat_count", "coder", "adjudicated"):
                continue
            r[c] = rec.get(c, "")
        named = [t for t in r["threat_models_named"].split(";") if t.strip()]
        # 0 means "full text read, no threat named"; blank means "not full-text coded".
        r["threat_count"] = len(named) if r["fulltext"] == "yes" else ""
        r["coder"] = "C1"
        r["adjudicated"] = "no"

    # Freeze C1's codes BEFORE the adjudication overlay, so the reliability
    # statistic compares C1's primary coding against C2, not the resolution.
    with open(os.path.join(AN, "coder1_codes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id"] + CODING_COLS)
        w.writeheader()
        for r in rows:
            if r["coder"] == "C1":
                w.writerow({"id": r["id"], **{c: r[c] for c in CODING_COLS}})

    for r in rows:
        ov = overlay.get(int(r["id"]))
        if not ov:
            continue
        for c, v in ov.items():
            r[c] = v
        named = [t for t in r["threat_models_named"].split(";") if t.strip()]
        r["threat_count"] = len(named) if r["fulltext"] == "yes" else ""
        r["adjudicated"] = "yes"

    with open(mpath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    ft = [r for r in rows if r["fulltext"] == "yes"]
    done_ft = [r for r in ft if r["coder"] == "C1"]
    print(f"coded {len(codes)} records; full-text coded {len(done_ft)}/{len(ft)}")
    print(f"adjudicated rows: {sum(1 for r in rows if r['adjudicated'] == 'yes')}")
    missing = sorted(int(r["id"]) for r in ft if r["coder"] != "C1")
    print("full-text ids still to code:", missing)


if __name__ == "__main__":
    main()
