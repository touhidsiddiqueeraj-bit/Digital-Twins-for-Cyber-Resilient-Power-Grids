#!/usr/bin/env python3
"""Generate the five manuscript figures from extraction_matrix.csv.

300 dpi, PDF (vector) + PNG (for review). Elsevier column widths: single 90 mm,
double 190 mm. Figures 2-5 read every number from the matrix; Figure 1 reproduces
the frozen screening counts recorded in prisma_flow.txt.
"""
import csv
import collections
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = os.environ.get("DTGRID_ROOT") or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

NAVY, TEAL, AMBER, GREY, RED = "#1F3864", "#2E8B8B", "#E8A33D", "#8C8C8C", "#B23A48"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 300})

rows = list(csv.DictReader(open(os.path.join(ROOT, "analysis", "extraction_matrix.csv"), encoding="utf-8")))
ft = [r for r in rows if r["fulltext"] == "yes"]
SCALE = {"0": "Not addressed", "1": "Mentioned", "2": "Substantive"}


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), bbox_inches="tight", dpi=300)
    plt.close(fig)
    print("wrote", name)


def fig1_prisma():
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    ax.axis("off")
    W, H = 3.1, 0.62
    boxes = [
        (2.6, 5.55, "Identification", "1,287 unique works\n(12 OpenAlex queries;\n2,000 incl. adversarial-AI probes)", NAVY),
        (2.6, 4.35, "Screening", "795 excluded — no digital-twin\nterm or no grid domain\n492 eligible", TEAL),
        (2.6, 3.15, "Eligibility", "392 excluded by relevance,\ncitation and recency ranking\n100 retained", AMBER),
        (1.1, 1.75, "Included — fully read", "83 records\n(full text coded in full)", "#3E6B3E"),
        (4.35, 1.75, "Included — abstract only", "17 records\n(full text not obtained)\nDOIs listed for access", RED),
    ]
    for x, y, title, body, col in boxes:
        ax.add_patch(FancyBboxPatch((x, y), W, H, boxstyle="round,pad=0.06,rounding_size=0.08",
                                    linewidth=1.2, edgecolor=col,
                                    facecolor=col, alpha=0.12, zorder=2))
        ax.text(x + W / 2, y + H - 0.16, title, ha="center", va="center",
                fontweight="bold", color=col, zorder=3)
        ax.text(x + W / 2, y + H / 2 - 0.16, body, ha="center", va="center", fontsize=7.4, zorder=3)
    for y0, y1 in ((5.55, 5.03), (4.35, 3.83), (3.15, 2.63)):
        ax.add_patch(FancyArrowPatch((2.6 + W / 2, y0), (2.6 + W / 2, y1),
                                     arrowstyle="-|>", mutation_scale=12, color="#333333"))
    ax.add_patch(FancyArrowPatch((2.6 + W / 2, 3.15), (1.1 + W / 2, 2.43),
                                 arrowstyle="-|>", mutation_scale=12, color="#333333"))
    ax.add_patch(FancyArrowPatch((2.6 + W / 2, 3.15), (4.35 + W / 2, 2.43),
                                 arrowstyle="-|>", mutation_scale=12, color="#333333"))
    ax.set_xlim(0.6, 7.9)
    ax.set_ylim(1.4, 6.5)
    save(fig, "fig1_prisma")


def fig2_year_venue():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9))
    yrs = sorted({int(r["year"]) for r in rows})
    counts = [sum(1 for r in rows if int(r["year"]) == y) for y in yrs]
    cols = [NAVY if y < 2025 else TEAL for y in yrs]
    a1.bar([str(y) for y in yrs], counts, color=cols)
    for i, c in enumerate(counts):
        a1.text(i, c + 0.6, str(c), ha="center", fontsize=7.5)
    a1.set_title("(a) Records by year (n=100)", fontsize=9)
    a1.set_ylabel("Records")
    a1.set_ylim(0, max(counts) * 1.18)

    vt = collections.Counter(r["venue_type"] for r in rows)
    order = ["journal", "conference", "thesis", "preprint", "report", "book_chapter"]
    vals = [vt.get(k, 0) for k in order]
    disp = [k.replace("_", " ") for k in order]
    a2.barh(disp[::-1], vals[::-1], color=[TEAL if k == "journal" else GREY for k in order[::-1]])
    for i, v in enumerate(vals[::-1]):
        a2.text(v + 0.4, i, str(v), va="center", fontsize=7.5)
    a2.set_title("(b) By venue type", fontsize=9)
    a2.set_xlim(0, max(vals) * 1.18)
    fig.tight_layout()
    save(fig, "fig2_year_venue")


def fig3_stance():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9),
                                 gridspec_kw={"width_ratios": [1.35, 1]})
    order = ["defensive", "review", "bridge", "enabling", "adversarial"]
    ftv = [sum(1 for r in ft if r["stance"] == s) for s in order]
    abv = [sum(1 for r in rows if r["fulltext"] == "no" and r["stance"] == s) for s in order]
    a1.bar(order, ftv, color=NAVY, label="full text (n=83)")
    a1.bar(order, abv, bottom=ftv, color=AMBER, label="abstract only (n=17)")
    for i, (f, a) in enumerate(zip(ftv, abv)):
        a1.text(i, f + a + 0.5, str(f + a), ha="center", fontsize=7.5)
    a1.set_title("(a) Stance, adjudicated coding (n=100)", fontsize=9)
    a1.set_ylabel("Records")
    a1.legend(fontsize=7)
    a1.tick_params(axis="x", rotation=20)

    seed = collections.Counter(r["stance_seed_from_openalex_screening"] for r in rows)
    coded = collections.Counter(r["stance"] for r in rows)
    x = range(len(order))
    a2.bar([i - 0.2 for i in x], [seed[s] for s in order], width=0.4, color=GREY, label="screening seed")
    a2.bar([i + 0.2 for i in x], [coded.get(s, 0) for s in order], width=0.4, color=TEAL, label="read coding")
    a2.set_xticks(list(x))
    a2.set_xticklabels(order, rotation=20)
    a2.set_title("(b) Seed vs read coding", fontsize=9)
    a2.legend(fontsize=7)
    fig.tight_layout()
    save(fig, "fig3_stance")


def fig4_threat_lifecycle():
    thr = ["fdi", "dos", "malware", "mitm", "replay", "false_command", "poisoning",
           "physical", "insider", "supply_chain", "evasion", "reverse_pathway"]
    life = ["design", "commissioning", "operation", "maintenance", "multi", "unclear"]
    M = [[sum(1 for r in ft if t in r["threat_models_named"].split(";") and r["lifecycle_stage"] == l)
          for l in life] for t in thr]
    fig, ax = plt.subplots(figsize=(4.3, 5.0))
    im = ax.imshow(M, cmap="Purples", aspect="auto", vmin=0)
    ax.set_xticks(range(len(life)))
    ax.set_xticklabels(life, rotation=35, ha="right", fontsize=8)
    ax.set_yticks(range(len(thr)))
    ax.set_yticklabels([t.replace("_", " ") for t in thr], fontsize=8)
    for i in range(len(thr)):
        for j in range(len(life)):
            v = M[i][j]
            ax.text(j, i, v if v else "·", ha="center", va="center", fontsize=7.5,
                    color="white" if v > 20 else "#222222")
    ax.set_title("Threat × lifecycle stage (n=83)", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.7, label="records")
    ax.set_xticks([x - 0.5 for x in range(1, len(life))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(thr))], minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="minor", length=0)
    fig.tight_layout()
    save(fig, "fig4_threat_lifecycle")


def fig5_ai_threats():
    vec = [("Adversarial ML", "ai_adv_ml"), ("Poisoning", "ai_poisoning"),
           ("Evasion", "ai_evasion"), ("LLM threats", "ai_llm"),
           ("Agentic automation", "ai_agentic"), ("Any AI-enabled", "ai_threat_overall")]
    labels = [v[0] for v in vec][::-1]
    zero = [sum(1 for r in ft if r[f] == "0") for _, f in vec][::-1]
    one = [sum(1 for r in ft if r[f] == "1") for _, f in vec][::-1]
    two = [sum(1 for r in ft if r[f] == "2") for _, f in vec][::-1]
    fig, ax = plt.subplots(figsize=(5.2, 3.1))
    y = range(len(labels))
    ax.barh(y, zero, color="#E4E4E4", label="0 · not addressed")
    ax.barh(y, one, left=zero, color=AMBER, label="1 · mentioned")
    ax.barh(y, two, left=[z + o for z, o in zip(zero, one)], color=NAVY, label="2 · substantive")
    for i, (z, o, t) in enumerate(zip(zero, one, two)):
        ax.text(z + o + t + 0.8, i, f"{o + t}  ({t})", va="center", fontsize=7.5)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Full-text records (n=83)")
    ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.22),
              ncol=3, frameon=False)
    ax.set_title("Engagement with AI-enabled threats", fontsize=9)
    ax.text(99, len(labels) - 0.35, "engaged (substantive)", ha="right", va="center",
            fontsize=6.6, color=GREY)
    fig.tight_layout()
    save(fig, "fig5_ai_threats")


if __name__ == "__main__":
    fig1_prisma(); fig2_year_venue(); fig3_stance()
    fig4_threat_lifecycle(); fig5_ai_threats()
