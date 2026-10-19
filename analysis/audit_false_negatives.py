#!/usr/bin/env python3
"""Audit the two headline claims for false negatives.

The extraction digest is keyword-windowed, so a paper that discusses an
AI-enabled threat without using the coded vocabulary would be silently missed.
This script re-reads the FULL text (reference list stripped) of every paper the
coder scored ai_threat_overall = 0, looking for an EXPANDED lexicon of
attacks-on-ML language. Any hit means the code may be wrong and needs a human
read.

Second audit: papers coded as naming no threat at all.
"""
import csv
import os
import re
import subprocess

ROOT = "/mnt/drive2/newpaper"
AN = os.path.join(ROOT, "analysis")

# Deliberately broader than the codebook: these are phrases that can only mean
# an attack on a model, a detector, or a training pipeline.
AI_ATTACK = {
    "adversarial example": r"adversarial\s+(?:example|sample)",
    "adversarial attack": r"adversarial\s+(?:attack|perturbation)",
    "adv ML": r"adversarial\s+machine\s+learning",
    "data poisoning": r"data\s+poisoning|poison\w*\s+(?:the\s+)?(?:data|training|model|dataset)",
    "backdoor": r"\bbackdoor\b",
    "model trojan": r"trojan\s+(?:model|neural|network)|(?:model|neural)\s+trojan",
    "evasion": r"evasion\s+attack|model\s+evasion|evade\s+(?:the\s+)?(?:detector|detection|IDS|classifier|model)",
    "membership inference": r"membership\s+inference",
    "model extraction": r"model\s+(?:extraction|stealing|inversion)",
    "label flipping": r"label\s+flipping|label\s+flip",
    "reward hacking": r"reward\s+hacking",
    "gradient attack": r"(?:gradient|weight)\s+(?:leak|attack|poisoning)",
    "prompt injection": r"prompt\s+injection|jailbreak",
    "LLM attack": r"(?:LLM|large\s+language\s+model)s?\b[^.]{0,60}\b(?:attack|exploit|malicious|manipulat)",
    "federated attack": r"federated\s+learning[^.]{0,60}\b(?:attack|poison|malicious|adversar)",
    "model manipulation": r"manipulat\w+\s+(?:the\s+)?(?:model|prediction|classifier|detector)",
}

# Generic threat language, for the "named no threat" audit.
GENERIC_THREAT = r"\battack|\bintrusion|\bexploit|\bmalicious|\bcompromis"

THRESH = 2  # hits of a single pattern before we insist on a look


def strip_refs(text):
    lines = text.split("\n")
    cut = None
    for i, ln in enumerate(lines):
        if re.match(r"^\s*(references|bibliography|works cited|references cited)\s*$", ln, re.I):
            cut = i
    return "\n".join(lines[:cut]) if cut else text


def text_of(path):
    try:
        t = subprocess.run(["pdftotext", "-q", os.path.join(ROOT, path), "-"],
                           capture_output=True, text=True, timeout=180).stdout
    except Exception:
        return ""
    return re.sub(r"\s+", " ", strip_refs(t))


def main():
    rows = list(csv.DictReader(open(os.path.join(AN, "extraction_matrix.csv"), encoding="utf-8")))
    ft = [r for r in rows if r["fulltext"] == "yes"]

    zero = [r for r in ft if r["ai_threat_overall"] == "0"]
    print(f"=== AUDIT 1: {len(zero)} records coded ai_threat_overall=0 ===")
    print("(looking for attacks-on-ML language the keyword window may have missed)\n")
    flagged = []
    for r in zero:
        t = text_of(r["local_path"])
        if not t:
            print(f"  !! {r['id']}: could not extract text")
            continue
        found = {k: len(re.findall(p, t, re.I)) for k, p in AI_ATTACK.items()}
        strong = {k: v for k, v in found.items() if v >= THRESH}
        if strong:
            flagged.append((r["id"], strong))
            print(f"  {r['id']:>3} | {r['venue'][:26]:26} | {strong}")
            for k in strong:
                m = re.search(AI_ATTACK[k], t, re.I)
                print(f"        {k}: ...{t[max(0,m.start()-120):m.end()+140].strip()}...")
    print(f"\n  -> {len(flagged)} of {len(zero)} zero-scored records need a human re-read")

    print(f"\n=== AUDIT 2: records coded as naming NO threat ===")
    none = [r for r in ft if not r["threat_models_named"].strip()]
    for r in none:
        t = text_of(r["local_path"])
        n = len(re.findall(GENERIC_THREAT, t, re.I))
        print(f"  {r['id']:>3} | {r['venue'][:26]:26} | generic threat-word hits: {n}")
    print(f"\n  -> {len(none)} records; a high generic hit count with an empty threat list "
          f"means the paper discusses attacks but names no threat model")


if __name__ == "__main__":
    main()
