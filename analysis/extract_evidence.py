#!/usr/bin/env python3
"""Build compact evidence digests from corpus PDFs to support human full-text coding.

Computer-assisted, human-coded. This script surfaces keyword hits and context snippets
ONLY. Every code in extraction_matrix.csv is assigned by a human reading these digests,
escalating to the full text where a call is ambiguous. The methodology section must
disclose this explicitly (see PAPER_PLAN.md Phase B).

Writes analysis/evidence/digest.txt
"""
import csv
import os
import re
import subprocess

ROOT = os.environ.get("DTGRID_ROOT") or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
AN = os.path.join(ROOT, "analysis")
EV = os.path.join(AN, "evidence")

GROUPS = {
    "THREAT": {
        "fdi": r"false[\s-]?data[\s-]?injection|\bFDI\b",
        "replay": r"replay",
        "dos": r"denial[\s-]of[\s-]service|\bDDoS?\b",
        "mitm": r"man[\s-]in[\s-]the[\s-]middle|\bMITM\b",
        "false_command": r"false[\s-]command|malicious[\s-]command|command[\s-]injection",
        "supply_chain": r"supply[\s-]chain",
        "hardware": r"hardware[\s-]trojan|hardware[\s-]implant",
        "physical": r"physical[\s-]attack|kinetic[\s-]attack|physical[\s-]intrusion",
        "insider": r"insider",
        "malware": r"malware|ransomware",
        "poisoning": r"poison|backdoor",
        "evasion": r"evasion|evasive",
        "prompt": r"prompt[\s-]injection|jailbreak",
        "reverse_pathway": r"reverse[\s-]attack|erroneous[\s-]command|malicious[\s-]commands?[\s-]to|back[\s-]to[\s-]the[\s-]physical|actuator",
    },
    "ML": {
        "machine_learning": r"machine[\s-]learning",
        "deep_learning": r"deep[\s-]learning",
        "neural": r"neural[\s-]network",
        "cnn": r"\bCNN\b|convolutional",
        "lstm": r"\bLSTM\b|long[\s-]short[\s-]term",
        "gnn": r"\bGNN\b|graph[\s-]neural",
        "svm": r"\bSVM\b|support[\s-]vector",
        "random_forest": r"random[\s-]forest",
        "autoencoder": r"auto[\s-]?encoder",
        "transformer": r"transformer[\s-](model|network|based)",
        "reinforcement": r"reinforcement[\s-]learning",
        "ensemble": r"ensemble",
        "xgboost": r"XGBoost|gradient[\s-]boost",
        "anomaly_detection": r"anomaly[\s-]detection",
    },
    "AITHRT": {
        "adversarial": r"adversarial[\s-](example|attack|machine|robust|training|perturbation|sample)",
        "poison": r"poison|backdoor",
        "evasion": r"evasion|evasive",
        "llm": r"large[\s-]language[\s-]model|\bLLM\b|\bGPT\b|prompt[\s-]injection",
        "agentic": r"agentic|autonomous[\s-]agent|multi[\s-]agent[\s-]attack",
        "generative": r"generative[\s-](ai|model)|\bGAN\b|deepfake",
    },
    "EVAL": {
        "rtds": r"\bRTDS\b|real[\s-]time[\s-]digital[\s-]simulat",
        "opalrt": r"OPAL[\s-]?RT|HYPERSIM",
        "hil": r"hardware[\s-]in[\s-]the[\s-]loop|\bHIL\b|power[\s-]hardware",
        "cosim": r"co[\s-]?simulat",
        "matlab": r"MATLAB|Simulink",
        "pscad": r"PSCAD|PowerFactory|PowerWorld|PSS[/\s-]?E",
        "gridlabd": r"GridLAB|OpenDSS|pandapower",
        "ieeebus": r"IEEE[\s-]?\d{1,3}[\s-]?(bus|node)",
        "testbed": r"testbed|test[\s-]bed|test[\s-]rig|test[\s-]bench|laborator",
        "field": r"field[\s-](trial|test|deployment)|real[\s-]world[\s-]deployment|pilot[\s-](study|project)",
    },
    "AVAIL": {
        "github": r"github|gitlab",
        "repo_other": r"zenodo|figshare|osf\.io",
        "code_avail": r"code[\s-]is[\s-]available|source[\s-]code|open[\s-]source|publicly[\s-]available",
        "data_avail": r"data[\s-]availability|dataset[\s-]is[\s-]available|public[\s-]dataset",
    },
    "LIFE": {
        "design": r"\bdesign[\s-](phase|stage)|\bplanning[\s-]phase|engineering[\s-]phase",
        "commissioning": r"commissioning",
        "operation": r"operational[\s-](phase|stage)|real[\s-]time[\s-]operation|in[\s-]service",
        "maintenance": r"maintenance|upgrade[\s-]phase",
        "decomm": r"decommission|end[\s-]of[\s-]life",
    },
    "RIGOR": {
        "metrics": r"\baccuracy\b|\bprecision\b|\brecall\b|\bF1\b|\bROC\b|\bAUC\b|false[\s-]positive|detection[\s-]rate",
        "baseline": r"baseline|compared[\s-](with|to|against)|benchmark",
        "limitation": r"limitation|future[\s-]work",
        "threatmodel": r"threat[\s-]model|attacker[\s-]model|adversary[\s-]model|attack[\s-]model",
        "adaptive": r"adaptive[\s-](attack|adversar)|moving[\s-]target|game[\s-]theoretic|Stackelberg|arms[\s-]race",
    },
}

AITHRT_ALL = True  # print zero-hit AI-threat terms too: absence is the finding


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def strip_refs(text):
    """Cut the reference list and author bios.

    Without this, cited titles inflate keyword counts — most damagingly for the
    AI-threat fields, which are the paper's headline measure. We keep everything
    before the LAST standalone References/Bibliography heading.
    """
    lines = text.split("\n")
    cut = None
    for i, ln in enumerate(lines):
        if re.match(r"^\s*(references|bibliography|works cited|references cited)\s*$",
                    ln, re.I):
            cut = i
    return "\n".join(lines[:cut]) if cut else text


def sniff(text, maxsnip=1):
    out = {}
    for grp, terms in GROUPS.items():
        rows = []
        for k, pat in terms.items():
            ms = list(re.finditer(pat, text, re.I))
            if ms:
                rows.append((k, len(ms),
                             collapse(text[max(0, ms[0].start() - 55):ms[0].end() + 65])))
            else:
                rows.append((k, 0, ""))
        out[grp] = rows
    return out


def main():
    os.makedirs(EV, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(AN, "extraction_matrix.csv"), encoding="utf-8")))
    full = [r for r in rows if r["fulltext"] == "yes"]
    lines = []
    thin = []
    for r in full:
        p = os.path.join(ROOT, r["local_path"])
        try:
            txt = subprocess.run(["pdftotext", "-q", p, "-"], capture_output=True,
                                 text=True, timeout=120).stdout
        except Exception as e:
            txt = ""
            thin.append((r["id"], f"pdftotext failed: {e}"))
        txt = strip_refs(txt)
        words = len(txt.split())
        if words < 1200:
            thin.append((r["id"], f"only {words} words extracted"))
        g = sniff(txt)
        head = (f"\n### {r['id']} | {r['year']} | {r['venue'][:38]} | {r['venue_type']} | "
                f"words={words} | {r['title'][:78]}")
        lines.append(head)
        for grp in ("THREAT", "AITHRT", "ML", "EVAL", "AVAIL", "LIFE", "RIGOR"):
            for k, n, s in g[grp]:
                if n == 0 and not (grp == "AITHRT"):
                    continue
                mark = f"{k}={n}"
                if s and n:
                    mark += f'  "{s[:128]}"'
                lines.append(f"  {grp:6s} {mark}")

    out = os.path.join(EV, "digest.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("papers digested :", len(full))
    print("digest lines    :", len(lines))
    print("digest bytes    :", os.path.getsize(out))
    print("\nthin extractions (review before coding):")
    for i, why in thin:
        print(f"  {i}: {why}")
    if not thin:
        print("  none")


if __name__ == "__main__":
    main()
