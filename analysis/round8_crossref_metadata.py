#!/usr/bin/env python3
"""Round-8: per-DOI Crossref metadata for the retained 100 (full abstracts).

The abstracts stored in digital_twin_grid_cybersecurity_papers.csv are
truncated (~250 chars); the text-level retrievability reconstruction of
round8_retrievability.py needs full title+abstract text, so this script
fetches authoritative Crossref metadata one DOI at a time and caches it.

Output: analysis/search_snapshot_2026-10-19/round8/retained100_crossref_metadata.csv
Columns: id, doi, crossref_doi, title, abstract, is-referenced-by-count,
container, type, year, http_status (ok | no-doi | not-found | error)
"""
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "analysis", "search_snapshot_2026-10-19", "round8")
os.makedirs(OUT, exist_ok=True)
DEST = os.path.join(OUT, "retained100_crossref_metadata.csv")

UA = {"User-Agent": "dt-powergrids-revision/1.0 (reproducibility package)"}


def norm_doi(d):
    d = (d or "").lower().strip()
    for pre in ("https://doi.org/", "http://doi.org/", "doi.org/", "doi:"):
        if d.startswith(pre):
            d = d[len(pre):]
    return d.strip()


def clean(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    matrix = list(csv.DictReader(open(os.path.join(ROOT, "analysis",
                     "extraction_matrix.csv"), encoding="utf-8")))
    existing = {}
    if os.path.exists(DEST):
        for r in csv.DictReader(open(DEST, encoding="utf-8")):
            existing[r["id"]] = r
    fields = ["id", "doi", "crossref_doi", "title", "abstract",
              "cited_by_crossref", "container", "type", "year", "http_status"]
    out = list(existing.values())
    done = {r["id"] for r in out}
    for m in matrix:
        rid = m["id"]
        if rid in done:
            continue
        doi = norm_doi(m["doi"])
        row = {"id": rid, "doi": m["doi"], "crossref_doi": "", "title": "",
               "abstract": "", "cited_by_crossref": "", "container": "",
               "type": "", "year": "", "http_status": ""}
        if not doi:
            row["http_status"] = "no-doi"
            out.append(row)
            continue
        url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                msg = json.loads(r.read().decode("utf-8"))["message"]
            row["crossref_doi"] = msg.get("DOI", "")
            row["title"] = clean((msg.get("title") or [""])[0])
            row["abstract"] = clean(msg.get("abstract") or "")
            row["cited_by_crossref"] = msg.get("is-referenced-by-count", "")
            row["container"] = clean((msg.get("container-title") or [""])[0])
            row["type"] = msg.get("type", "")
            dp = (msg.get("issued", {}).get("date-parts") or [[None]])[0]
            row["year"] = str(dp[0]) if dp and dp[0] else ""
            row["http_status"] = "ok" if row["abstract"] else "ok-no-abstract"
        except Exception as e:  # noqa: BLE001
            row["http_status"] = f"error:{type(e).__name__}"
        out.append(row)
        time.sleep(0.25)
    with open(DEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in sorted(out, key=lambda r: int(r["id"])):
            w.writerow(r)
    ok = sum(1 for r in out if r["http_status"].startswith("ok"))
    noabs = sum(1 for r in out if r["http_status"] == "ok-no-abstract")
    print(f"retained-100 Crossref lookups: ok={ok} (without abstract: {noabs}), "
          f"failed={len(out)-ok}")


if __name__ == "__main__":
    main()
