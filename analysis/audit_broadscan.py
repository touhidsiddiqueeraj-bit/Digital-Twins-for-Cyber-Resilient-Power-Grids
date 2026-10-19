#!/usr/bin/env python3
"""Broad-net re-scan of the records coded ai_threat_overall = 0.

The digest builder (extract_evidence.py) and audit_false_negatives.py both require
AI-threat-SPECIFIC vocabulary ("adversarial example", "data poisoning", "backdoor").
A paper that attacks the ML/DT component only in generic words ("the adversary
manipulates the model's inputs", "stealthy tampering") fires neither instrument and
would be coded 0 in good faith.

This scan casts a deliberately WIDE net over attacks-on-the-AI-component language and
prints the windows, so a human can adjudicate each one. Hits are grouped by how many
distinct families fire; most-suspect first. Output is for reading, not for counting:
the point is to estimate the false-negative rate of the 0 code, not to auto-recant it.
"""
import csv
import os
import re
import subprocess

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AN = os.path.join(ROOT, "analysis")

# Each family is a broad indication that the AI/ML/DT component itself is under attack.
FAMILIES = {
    "adversar*": r"adversar\w*",
    "poison/backdoor": r"poison\w*|\bbackdoor\w*|\btrojan\w*",
    "evasion": r"evasion|evade\w*|evasive",
    "model-manip": r"manipulat\w{0,3}\s+(?:the\s+)?(?:model|learn|classif|detect|predict|train|input|feature|data|measurement|reading)",
    "model-compromise": r"(?:tamper|spoof|falsif|corrupt|compromis|deceiv|inject)\w{0,3}\s+(?:the\s+)?(?:model|learn|classif|detect|predict|train|input|feature|data|measurement|reading|signal)",
    "integrity-attack": r"integrity\s+attack|attack.{0,15}integrity|data\s+integrity",
    "stealthy": r"stealth\w*",
    "generative": r"generative\s+(?:ai|model|adversar)|\bGAN\b|deepfake|synthetic\s+(?:attack|data)\s+generat",
    "llm": r"large\s+language\s+model|\bLLM\b|\bGPT\b|prompt\s+injection|jailbreak",
    "unseen-attack": r"unseen\s+attack|unknown\s+attack|novel\s+attack|zero[\s-]day",
}


def strip_refs(text):
    lines = text.split("\n")
    cut = None
    for i, ln in enumerate(lines):
        if re.match(r"^\s*(references|bibliography|works cited|references cited)\s*$", ln, re.I):
            cut = i
    return "\n".join(lines[:cut]) if cut else text


def main():
    rows = list(csv.DictReader(open(os.path.join(AN, "extraction_matrix.csv"), encoding="utf-8")))
    zero = [r for r in rows if r["fulltext"] == "yes" and r["ai_threat_overall"] == "0"]
    print(f"broad-net scan of {len(zero)} records coded ai_threat_overall=0\n")

    flagged = []
    for r in zero:
        try:
            raw = subprocess.run(["pdftotext", "-q", os.path.join(ROOT, r["local_path"]), "-"],
                                 capture_output=True, text=True, timeout=180).stdout
        except Exception:
            continue
        t = re.sub(r"\s+", " ", strip_refs(raw))
        fam = {}
        for name, pat in FAMILIES.items():
            ms = list(re.finditer(pat, t, re.I))
            if ms:
                fam[name] = (len(ms), ms)
        if fam:
            flagged.append((len(fam), r, fam, t))  # keep t: offsets are only valid against it

    flagged.sort(key=lambda x: -x[0])
    for nfam, r, fam, t in flagged:
        print(f"{'='*78}")
        print(f"id {r['id']} | {nfam} families | {r['venue'][:44]} | {r['title'][:70]}")
        print(f"  coded: ai_threat_overall=0  adv={r['ai_adv_ml']} poison={r['ai_poisoning']} "
              f"evasion={r['ai_evasion']} llm={r['ai_llm']} agentic={r['ai_agentic']}")
        for name, (cnt, ms) in sorted(fam.items(), key=lambda x: -x[1][0]):
            print(f"  [{name}] x{cnt}")
            for m in ms[:2]:
                w = re.sub(r"\s+", " ", t[max(0, m.start() - 130):m.end() + 190]).strip()
                print(f"      ...{w}...")
    print(f"\nflagged {len(flagged)} of {len(zero)} zero-coded records for adjudication")


if __name__ == "__main__":
    main()
