#!/usr/bin/env python3
"""Verify every corpus DOI against Crossref, falling back to DataCite.

Writes analysis/doi_verification_all.csv.
Polite pool: identifies itself with a mailto per Crossref etiquette.
"""
import csv
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

ROOT = os.environ.get("DTGRID_ROOT") or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
OUT = os.path.join(ROOT, "analysis", "doi_verification_all.csv")
UA = "dtreview-doi-verifier/1.0 (mailto:research@example.org)"


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def from_crossref(doi):
    d = fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    title = (d.get("title") or [""])[0]
    year = None
    for k in ("published-print", "published-online", "issued", "created"):
        if d.get(k, {}).get("date-parts", [[None]])[0][0]:
            year = d[k]["date-parts"][0][0]
            break
    venue = (d.get("container-title") or [""])[0] or d.get("publisher", "")
    return title, year, venue, d.get("type", "")


def from_datacite(doi):
    d = fetch("https://api.datacite.org/dois/" + urllib.parse.quote(doi))["data"]["attributes"]
    title = (d.get("titles") or [{}])[0].get("title", "")
    year = d.get("publicationYear")
    venue = d.get("publisher") or ""
    return title, year, venue, d.get("types", {}).get("resourceTypeGeneral", "")


def check_handle(doi):
    """Authoritative existence test: the global DOI handle system.

    A DOI can be registered and resolvable while its metadata has not yet been
    indexed by Crossref/DataCite. Returns (exists, url_or_"").
    """
    try:
        req = urllib.request.Request(
            "https://doi.org/api/handles/" + doi,
            headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8", "ignore"))
        if d.get("responseCode") == 1:
            urls = [v["data"]["value"] for v in d.get("values", []) if v.get("type") == "URL"]
            return True, (urls[0] if urls else "")
    except Exception:
        pass
    return False, ""


def main():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "downloads_manifest.csv"), encoding="utf-8")))
    done = {}
    if os.path.exists(OUT):
        for x in csv.DictReader(open(OUT, encoding="utf-8")):
            if x["status"] in ("verified", "no_doi", "not_registered", "registered_no_metadata"):
                done[x["id"]] = x
    out = []
    for i, r in enumerate(rows, 1):
        if str(i) in done:
            out.append(done[str(i)])
            continue
        doi = (r["doi_clean"] or "").strip()
        rec = {"id": i, "doi": doi, "source": "", "status": "", "http_status": "",
               "registered_title": "", "registered_year": "", "registered_venue": "",
               "registered_type": "", "title_match": "", "resolved_url": ""}
        if not doi:
            rec.update(source="none", status="no_doi")
            out.append(rec)
            continue
        title = year = venue = rtype = None
        src = ""
        try:
            title, year, venue, rtype = from_crossref(doi)
            src = "crossref"
        except urllib.error.HTTPError as e:
            rec["http_status"] = str(e.code)
            if e.code == 404:
                try:
                    title, year, venue, rtype = from_datacite(doi)
                    src = "datacite"
                except urllib.error.HTTPError as e2:
                    rec["http_status"] += "/" + str(e2.code)
        except Exception as e:
            rec["http_status"] = type(e).__name__
        if not src:
            exists, resolved = check_handle(doi)
            if exists:
                rec.update(source="handle", status="registered_no_metadata", resolved_url=resolved)
                print(f"  {i:3d} REGISTERED (no metadata)  {doi}  -> {resolved[:60]}")
            else:
                rec.update(source="none", status="not_registered")
                print(f"  {i:3d} NOT REGISTERED  {doi}")
            out.append(rec)
            time.sleep(0.35)
            continue
        a, b = norm(r["title"]), norm(title)
        if a and a == b:
            match = "exact"
        elif a and b and (a in b or b in a or SequenceMatcher(None, a, b).ratio() > 0.85):
            match = "near"
        else:
            match = "none"
        rec.update(source=src, status="verified", registered_title=title,
                   registered_year=year or "", registered_venue=venue or "",
                   registered_type=rtype or "", title_match=match)
        out.append(rec)
        flag = "" if match == "exact" else f"  [{match}]"
        print(f"  {i:3d} {src:9s} {match:5s} {doi}{flag}")
        time.sleep(0.35)

    cols = ["id", "doi", "source", "status", "http_status", "registered_title",
            "registered_year", "registered_venue", "registered_type", "title_match", "resolved_url"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    print("\nwrote", OUT)
    print("status:", dict(Counter(x["status"] for x in out)))
    print("source:", dict(Counter(x["source"] for x in out)))
    print("title match:", dict(Counter(x["title_match"] for x in out if x["status"] == "verified")))
    print("handle-resolvable:", dict(Counter(x["status"] for x in out)))


if __name__ == "__main__":
    main()
