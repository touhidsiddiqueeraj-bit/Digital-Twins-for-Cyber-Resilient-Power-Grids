#!/usr/bin/env python3
"""Round-8 text-level retrievability reconstruction (Item 1).

The original OpenAlex per-record query provenance was not retained and OpenAlex
re-runs remain blocked, so this script re-executes the *semantics* of the 16
query strings against each retained record's own retrievable text. A record is
"retrievable by a query (reconstruction)" if every phrase component of that
query occurs in the record's title and abstract (variant A), or additionally in
the released full-text keyword windows (variant B, generous).

Phrase components are matched case-insensitively with declared, minimal
normalisation: hyphen/space equivalence and optional plural 's'
("digital twin(s)", "cyber-attack", "smart-grids"); "cybersecurity" also
matches "cyber security"; "cyber attack" also matches "cyberattack(s)".

Classification per variant:
  probe-only   = at least one probe query matches, no core query matches
  core-only    = at least one core query matches, no probe query matches
  both         = both families match
  neither      = no query matches

The headline fields (any/substantive engagement, ML use) are then re-run on the
probe-only subset of the 83 full-text records.

Output: analysis/search_snapshot_2026-10-19/round8/retrievability_textlevel.csv
"""
import csv
import json
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "analysis", "search_snapshot_2026-10-19")
OUT = os.path.join(SNAP, "round8")
RUN_DATE = "2026-10-19"

# phrase -> regex, with declared normalisation
PHRASE_RES = {
    "digital twin": r"digital[\s-]*twins?",
    "power grid": r"power[\s-]*grids?",
    "smart grid": r"smart[\s-]*grids?",
    "power system": r"power[\s-]*systems?",
    "energy system": r"energy[\s-]*systems?",
    "cybersecurity": r"cyber[\s-]*security|cybersecurity",
    "cyber attack": r"cyber[\s-]*attacks?|cyberattacks?",
    "intrusion detection": r"intrusion[\s-]*detection",
    "adversarial machine learning": r"adversarial[\s-]*machine[\s-]*learning",
    "data poisoning": r"data[\s-]*poisoning",
    "adversarial examples": r"adversarial[\s-]*examples?",
    "large language model": r"large[\s-]*language[\s-]*models?",
}


def compile_query(string):
    """Return (label, [regex]) for every phrase/token component of the string."""
    parts = re.findall(r'"([^"]+)"|(\b[a-z]+\b)', string)
    comps = []
    for quoted, bare in parts:
        term = (quoted or bare).lower().strip()
        if term in ("and", "or", "dt"):
            continue
        comps.append(term)
    res = []
    for t in comps:
        if t in PHRASE_RES:
            res.append(re.compile(PHRASE_RES[t], re.I))
        else:
            res.append(re.compile(re.escape(t), re.I))
    return comps, res


def digest_windows(record_id):
    """Extract the released full-text keyword windows for a record from digest.txt."""
    path = os.path.join(ROOT, "analysis", "evidence", "digest.txt")
    txt = globals()["_DIGEST_CACHE"]
    m = re.search(r"^### %s \|.*?(?=^### \d+ \||\Z)" % record_id, txt, re.S | re.M)
    if not m:
        return ""
    return m.group(0)


def main():
    queries = json.load(open(os.path.join(SNAP, "queries.json"),
                            encoding="utf-8"))["queries"]
    compiled = {q["id"]: compile_query(q["string"]) for q in queries}
    core_ids = [q["id"] for q in queries if q.startswith("core-")] if False \
        else [q["id"] for q in queries if q["id"].startswith("core-")]
    probe_ids = [q["id"] for q in queries if q["id"].startswith("probe-")]

    with open(os.path.join(ROOT, "analysis", "evidence", "digest.txt"),
              encoding="utf-8") as f:
        globals()["_DIGEST_CACHE"] = f.read()

    matrix = {r["id"]: r for r in csv.DictReader(
        open(os.path.join(ROOT, "analysis", "extraction_matrix.csv"),
             encoding="utf-8"))}
    meta = {r["id"]: r for r in csv.DictReader(
        open(os.path.join(OUT, "retained100_crossref_metadata.csv"),
             encoding="utf-8"))}
    papers = list(csv.DictReader(
        open(os.path.join(ROOT, "digital_twin_grid_cybersecurity_papers.csv"),
             encoding="utf-8")))
    stored_abstract = {}
    # papers CSV row order = ID order 1..100 (display order)
    for i, p in enumerate(papers, start=1):
        stored_abstract[str(i)] = p.get("abstract", "")

    rows = []
    for rid in range(1, 101):
        m = matrix[str(rid)]
        title = m["title"]
        cr = meta.get(str(rid), {})
        abstract = cr.get("abstract") or stored_abstract.get(str(rid), "")
        text_a = title + "\n" + abstract
        text_b = text_a + "\n" + digest_windows(str(rid))

        def matching(text, qids):
            out = []
            for qid in qids:
                comps, res = compiled[qid]
                if all(r.search(text) for r in res):
                    out.append(qid)
            return out

        core_a = matching(text_a, core_ids)
        probe_a = matching(text_a, probe_ids)
        core_b = matching(text_b, core_ids)
        probe_b = matching(text_b, probe_ids)

        def cls(core, probe):
            if core and probe:
                return "both"
            if core:
                return "core_only"
            if probe:
                return "probe_only"
            return "neither"

        rows.append({
            "id": rid, "title": title[:110], "fulltext": m["fulltext"],
            "ai_threat_overall": m["ai_threat_overall"],
            "abstract_source": "crossref" if cr.get("abstract") else
                               ("stored" if stored_abstract.get(str(rid)) else "none"),
            "A_core_queries": ";".join(core_a),
            "A_probe_queries": ";".join(probe_a),
            "A_class": cls(core_a, probe_a),
            "B_core_queries": ";".join(core_b),
            "B_probe_queries": ";".join(probe_b),
            "B_class": cls(core_b, probe_b),
        })

    with open(os.path.join(OUT, "retrievability_textlevel.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    for variant in ("A", "B"):
        c_all = Counter(r[f"{variant}_class"] for r in rows)
        c_ft = Counter(r[f"{variant}_class"] for r in rows if r["fulltext"] == "yes")
        print(f"\nVariant {variant} ({'title+abstract' if variant=='A' else '+full-text windows'}) "
              f"classes, all 100:", dict(c_all), "| full-text 83:", dict(c_ft))
        po_ids = [r["id"] for r in rows
                  if r[f"{variant}_class"] == "probe_only" and r["fulltext"] == "yes"]
        print(f"  probe-only full-text ids: {po_ids}")
        sub = [r for r in rows if r[f"{variant}_class"] == "probe_only"
               and r["fulltext"] == "yes"]
        if sub:
            n = len(sub)
            any_ = sum(1 for r in sub if r["ai_threat_overall"] in ("1", "2"))
            subst = sum(1 for r in sub if r["ai_threat_overall"] == "2")
            print(f"  probe-only subset: n={n} any={any_} ({any_/n*100:.0f}%) "
                  f"subst={subst} ({subst/n*100:.0f}%)")
        # engagement restricted to records retrievable by core in variant
        co = [r for r in rows if r[f"{variant}_class"] in ("core_only", "both")
              and r["fulltext"] == "yes"]
        if co:
            n = len(co)
            any_ = sum(1 for r in co if r["ai_threat_overall"] in ("1", "2"))
            subst = sum(1 for r in co if r["ai_threat_overall"] == "2")
            print(f"  core-retrievable subset: n={n} any={any_} "
                  f"({any_/n*100:.1f}%) subst={subst} ({subst/n*100:.1f}%)")
        # which engaged records are probe-retrievable at all
        eng_probe = [r["id"] for r in rows if r["ai_threat_overall"] in ("1", "2")
                     and r[f"{variant}_probe_queries"]]
        eng_sub_probe = [r["id"] for r in rows if r["ai_threat_overall"] == "2"
                         and r[f"{variant}_probe_queries"]]
        print(f"  engaged records probe-retrievable: {eng_probe}")
        print(f"  substantive records probe-retrievable: {eng_sub_probe}")


if __name__ == "__main__":
    main()
