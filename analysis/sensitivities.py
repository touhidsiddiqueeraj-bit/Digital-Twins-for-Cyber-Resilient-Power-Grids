#!/usr/bin/env python3
"""Verification and sensitivity analyses.

Computes the data-dependent quantities behind the manuscript's sensitivity
sections:
  1. Parse analysis/evidence/broadscan.txt -> strong/weak firing classification,
     identify the 15 weak-only firings (and the 10 non-firing negatives).
  2. Core-subset concentration: all 16 any-engagers among the 41 security-primary
     non-review studies fall inside the 29-study core subset?
  3. Cited vs zero-citation engagement rates (quality sensitivity).
  4. Substantive by venue type (document-length proxy for the depth instrument).
  5. R69-exclusion sensitivities (unattributed, out-of-scope, substantive).
  6. threat_models_named vs ai_* overlap (poisoning/evasion/prompt).
  7. twin_role distribution + near-constancy of tool default.
"""
import csv
import os
import re
from collections import Counter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AN = os.path.join(ROOT, "analysis")

STRONG = {"poison/backdoor", "model-manip", "model-compromise", "evasion"}

rows = list(csv.DictReader(open(os.path.join(AN, "extraction_matrix.csv"), encoding="utf-8")))
by_id = {r["id"]: r for r in rows}
full = [r for r in rows if r["fulltext"] == "yes"]
print(f"matrix n={len(rows)}  full-text={len(full)}")

# ---------- 1. parse broadscan.txt ----------
txt = open(os.path.join(AN, "evidence", "broadscan.txt"), encoding="utf-8").read()
blocks = re.split(r"={78}", txt)
entries = {}
for b in blocks:
    m = re.match(r"\s*id (\d+) \| (\d+) families \| (.*?) \| (.*)\n\s*coded:.*", b, re.S)
    if not m:
        continue
    rid, nfam = m.group(1), int(m.group(2))
    fams = re.findall(r"^\s*\[([a-z\-\*/]+)\] x(\d+)", b, re.M)
    entries[rid] = {"nfam": nfam, "fams": [f for f, _ in fams],
                    "block": b, "title": m.group(4).strip()[:70]}

neg = [r for r in full if r["ai_threat_overall"] == "0"]
neg_ids = {r["id"] for r in neg}
strong_ids = {rid for rid, e in entries.items() if any(f in STRONG for f in e["fams"])}
weak_only = {rid for rid, e in entries.items()
             if rid not in strong_ids and any(f not in STRONG for f in e["fams"])}
fired_none = neg_ids - set(entries)

print(f"\n--- broadscan parse: {len(entries)} entries of {len(neg)} negatives")
print(f"strong firings: {len(strong_ids)} | weak-only firings: {len(weak_only)} | no firing: {len(fired_none)}")
print(f"weak-only ids: {sorted(weak_only, key=int)}")
print(f"no-firing ids: {sorted(fired_none, key=int)}")
# cross-check: strong + weak == 38?
assert len(entries) == len(strong_ids | weak_only), (len(entries), len(strong_ids), len(weak_only))

# ---------- 2. core-subset concentration ----------
sp = [r for r in full if r["security_primary"] == "yes" and r["stance"] != "review"]
any_sp = [r for r in sp if r["ai_threat_overall"] in ("1", "2")]
core = [r for r in sp if r["ml_role"] == "detection"]
any_core = [r for r in core if r["ai_threat_overall"] in ("1", "2")]
out = [r["id"] for r in any_sp if r["id"] not in {c["id"] for c in core}]
print(f"\n--- concentration: sec-prim non-review n={len(sp)}, any={len(any_sp)}; "
      f"core (detection-ML) n={len(core)}, any={len(any_core)}")
print(f"any-engagers OUTSIDE core subset: {out or 'NONE - all inside'}")
print(f"stance values in sp: {Counter(r['stance'] for r in sp)}")

# ---------- 3. cited vs zero-citation ----------
for label, sel in [("cited>0", lambda r: int(r["cited_by"] or 0) > 0),
                   ("cited=0", lambda r: int(r["cited_by"] or 0) == 0)]:
    sub = [r for r in full if sel(r)]
    any_ = [r for r in sub if r["ai_threat_overall"] in ("1", "2")]
    subst = [r for r in sub if r["ai_threat_overall"] == "2"]
    print(f"{label}: n={len(sub)}  any={len(any_)} ({len(any_)/len(sub)*100:.1f}%)  "
          f"subst={len(subst)} ({len(subst)/len(sub)*100:.1f}%)")
zero_ids = [r["id"] for r in full if int(r["cited_by"] or 0) == 0]
print(f"zero-citation full-text ids: {zero_ids}")

# ---------- 4. substantive by venue type (length proxy) ----------
print("\n--- engagement by venue_type (full text):")
for vt in sorted({r["venue_type"] for r in full}):
    sub = [r for r in full if r["venue_type"] == vt]
    any_ = sum(1 for r in sub if r["ai_threat_overall"] in ("1", "2"))
    subst = sum(1 for r in sub if r["ai_threat_overall"] == "2")
    print(f"  {vt:14s} n={len(sub):3d}  any={any_:3d}  subst={subst:2d}")

# ---------- 5. R69 exclusion ----------
subst_ids = [r["id"] for r in full if r["ai_threat_overall"] == "2"]
print(f"\nsubstantive ids: {subst_ids}")
subst_core = [r["id"] for r in core if r["ai_threat_overall"] == "2"]
print(f"substantive in core: {subst_core}")
print(f"R69 in substantive: {'69' in subst_ids}; in core substantive: {'69' in subst_core}")
print(f"excl R69: 83 -> 82, subst {len(subst_ids)} -> {len(subst_ids) - ('69' in subst_ids)}; "
      f"core 29 -> 28, subst {len(subst_core)} -> {len(subst_core) - ('69' in subst_core)}")
# R69 authors/venue check
r69 = by_id["69"]
print(f"R69 authors='{r69['authors'].strip()[:60]}' venue='{r69['venue'][:60]}' stance={r69['stance']}")
r18 = by_id["18"]
print(f"R18 authors='{r18['authors'].strip()[:60]}'")

# ---------- 6. threat_models_named vs ai_* overlap ----------
def threat_set(r):
    return set(t.strip() for t in re.split(r"[;,]", r["threat_models_named"]) if t.strip())
ov = {}
for name, aif in [("poisoning", "ai_poisoning"), ("evasion", "ai_evasion"), ("prompt", "ai_llm")]:
    named = [r for r in full if name in threat_set(r)]
    ai_any = [r for r in named if r[aif] in ("1", "2")]
    ai_sub = [r for r in named if r[aif] == "2"]
    # ai-engaged but not named in vocabulary
    ai_only = [r for r in full if r[aif] in ("1", "2") and name not in threat_set(r)]
    ov[name] = (len(named), len(ai_any), len(ai_sub), len(ai_only))
    print(f"\n{name}: named-in-vocabulary={len(named)}, of which ai_{name}>=1: {len(ai_any)} "
          f"(subst {len(ai_sub)}); ai_{name}>=1 but NOT named: {len(ai_only)}")
    print(f"  named-but-not-ai ids: {[r['id'] for r in named if r[aif]=='0']}")

# ---------- 7. twin_role near-constancy ----------
tr = Counter(r["twin_role"] for r in full)
print(f"\ntwin_role distribution: {dict(tr)}  tool share={tr['tool']/len(full)*100:.1f}%")

# stance review share of 100
st = Counter(r["stance"] for r in rows)
print(f"stance over 100: {dict(st)}")
print(f"reviews among full text: {sum(1 for r in full if r['stance']=='review')}")
