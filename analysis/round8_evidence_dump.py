#!/usr/bin/env python3
"""Round-8: assemble per-record evidence for the independent (AI-instrument)
readback of the headline field (Item 4) and the direction split (Item 6).

For each of the 83 full-text-coded records this writes one block containing:
  - id, title, venue type, coded stance (for orientation only),
  - the full abstract (Crossref full text where fetched, else the stored
    abstract),
  - the released full-text keyword windows most relevant to AI-threat
    engagement: every AITHRT window (adversarial/poison/evasion/llm/agentic/
    generative), the poisoning/evasion/prompt THREAT windows, the first ML
    window for defensive context, plus -- for records coded 0 -- every
    broad-scan audit family window.

The dump is the reading basis for analysis/reliability/readback_ai_codes.csv
and is released so that each judgement in that file can be checked against
the same evidence.

Output: analysis/reliability/readback_evidence_dump.txt
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPR8 = os.path.join(ROOT, "analysis", "search_snapshot_2026-10-19", "reconstruction")
OUT = os.path.join(ROOT, "analysis", "reliability",
                   "readback_evidence_dump.txt")

digest = open(os.path.join(ROOT, "analysis", "evidence", "digest.txt"),
              encoding="utf-8").read()
broad = open(os.path.join(ROOT, "analysis", "evidence", "broadscan.txt"),
             encoding="utf-8").read()


def digest_block(rid):
    m = re.search(r"^### %s \|.*?(?=^### \d+ \||\Z)" % rid, digest, re.S | re.M)
    return m.group(0) if m else ""


def broad_block(rid):
    m = re.search(r"^id %s \|[^\n]*\n\s*coded:.*?(?=^={20,}|\Z)" % rid,
                  broad, re.S | re.M)
    return m.group(0) if m else ""


def trim(s, n=150):
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n] + ("…" if len(s) > n else "")


def main():
    matrix = {r["id"]: r for r in csv.DictReader(open(
        os.path.join(ROOT, "analysis", "extraction_matrix.csv"),
        encoding="utf-8"))}
    meta = {r["id"]: r for r in csv.DictReader(open(
        os.path.join(SNAPR8, "retained100_crossref_metadata.csv"),
        encoding="utf-8"))}
    papers = list(csv.DictReader(open(
        os.path.join(ROOT, "digital_twin_grid_cybersecurity_papers.csv"),
        encoding="utf-8")))

    out = []
    full_ids = [r["id"] for r in matrix.values() if r["fulltext"] == "yes"]
    for rid in sorted(full_ids, key=int):
        m = matrix[rid]
        cr = meta.get(rid, {})
        abstract = cr.get("abstract") or papers[int(rid) - 1].get("abstract", "")
        out.append("=" * 100)
        out.append(f"RECORD {rid} | {m['venue_type']} | {m['year']} | "
                   f"coded stance: {m['stance']}")
        out.append(f"TITLE: {m['title']}")
        out.append(f"ABSTRACT ({'crossref-full' if cr.get('abstract') else 'stored'}): "
                   f"{trim(abstract, 600)}")
        db = digest_block(rid)
        ai_lines = re.findall(r"^\s*AITHRT .*$", db, re.M)
        th_lines = re.findall(r"^\s*THREAT (poisoning|evasion|prompt|other)=\d+.*$",
                              db, re.M | re.I)
        th_all = [l for l in re.findall(r"^\s*THREAT .*$", db, re.M)
                  if re.match(r"\s*THREAT (poisoning|evasion|prompt|other)=",
                              l, re.I)]
        ml_lines = re.findall(r"^\s*ML .*$", db, re.M)[:2]
        out.append("AI-RELEVANT FULL-TEXT WINDOWS (from digest.txt):")
        if ai_lines or th_all:
            for l in ai_lines + th_all:
                out.append("   " + trim(l, 165))
        else:
            out.append("   (no AI-family windows fired)")
        for l in ml_lines:
            out.append("   " + trim(l, 130))
        if m["ai_threat_overall"] == "0":
            bb = broad_block(rid)
            out.append("BROAD-SCAN AUDIT WINDOWS (negatives only, from broadscan.txt):")
            fams = re.findall(r"^\s*\[([a-z\-\*/]+)\] x(\d+)", bb, re.M)
            if not fams:
                out.append("   (no broad-scan family fired)")
            for fam, cnt in fams:
                wtext = re.search(r"\[%s\] x%s\n(.*?)(?=^\s*\[|\Z)" % (fam, cnt),
                                  bb, re.S | re.M)
                w1 = wtext.group(1) if wtext else ""
                w1 = trim(re.sub(r"\s+", " ", w1), 150)
                out.append(f"   [{fam}] x{cnt}: {w1}")
        out.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"wrote {OUT}: {len(out)} lines for {len(full_ids)} records")


if __name__ == "__main__":
    main()
