#!/usr/bin/env python3
"""Round-8 statistics: venue-format re-scoring (Item 5), strict-scope
equivalents (Item 7), light quality appraisal (Item 9).

Outputs:
  analysis/quality_appraisal.csv  -- per-record quality signals
  console tables quoted in the manuscript revision
"""
import csv
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AN = os.path.join(ROOT, "analysis")

try:
    from scipy.stats import fisher_exact
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False


def fisher(a, b, c, d):
    """2x2 Fisher exact, one-sided (greater), computed exactly if no scipy."""
    if HAVE_SCIPY:
        _, p = fisher_exact([[a, b], [c, d]], alternative="greater")
        return p
    # manual: hypergeometric tail
    from math import comb
    n = a + b + c + d
    r1 = a + b
    denom = comb(n, r1)
    num = 0.0
    k = a
    while k <= min(r1, a + c):
        num += comb(a + c, k) * comb(b + d, r1 - k)
        k += 1
    return num / denom


def main():
    rows = list(csv.DictReader(open(os.path.join(AN, "extraction_matrix.csv"),
                                    encoding="utf-8")))
    full = [r for r in rows if r["fulltext"] == "yes"]

    # ---------------- Item 5: venue-format re-scoring -----------------
    print("=== Item 5: engagement by venue format (full text, n=83) ===")
    fmt_stats = {}
    for vt in sorted({r["venue_type"] for r in full}):
        sub = [r for r in full if r["venue_type"] == vt]
        any_ = sum(1 for r in sub if r["ai_threat_overall"] in ("1", "2"))
        sub_ = sum(1 for r in sub if r["ai_threat_overall"] == "2")
        nonrev = [r for r in sub if r["stance"] != "review"]
        nr_any = sum(1 for r in nonrev if r["ai_threat_overall"] in ("1", "2"))
        nr_sub = sum(1 for r in nonrev if r["ai_threat_overall"] == "2")
        fmt_stats[vt] = (len(sub), any_, sub_, len(nonrev), nr_any, nr_sub)
        print(f"{vt:12s} n={len(sub):2d} any={any_:2d} ({any_/len(sub)*100:5.1f}%) "
              f"subst={sub_:2d} ({sub_/len(sub)*100:5.1f}%) | non-review n={len(nonrev):2d} "
              f"any={nr_any} subst={nr_sub}")
    j = fmt_stats["journal"]
    c = fmt_stats["conference"]
    p_fish_sub = fisher(j[2], j[0] - j[2], c[2], c[0] - c[2])
    p_fish_any = fisher(j[1], j[0] - j[1], c[1], c[0] - c[1])
    print(f"Fisher exact (journal vs conference, substantive): p={p_fish_sub:.3f}")
    print(f"Fisher exact (journal vs conference, any): p={p_fish_any:.3f}")
    # within non-review journals vs conferences
    pj = fisher(j[5], j[3] - j[5], c[5], c[3] - c[5])
    print(f"Fisher exact (non-review journal vs conference, substantive): p={pj:.3f}")
    # page-count style length proxy is unavailable; report within-format only
    thesis_pre = fmt_stats.get("preprint")
    print("preprint fmt:", thesis_pre, "thesis:", fmt_stats.get("thesis"),
          "book_chapter:", fmt_stats.get("book_chapter"),
          "report:", fmt_stats.get("report"))

    # ---------------- Item 7: strict-scope equivalents ----------------
    print("\n=== Item 7: strict-scope equivalents ===")
    OUT_IDS = {"18", "59", "69", "97"}
    strict = [r for r in full if r["id"] not in OUT_IDS]

    def interface_or_model(r):
        t = set(x.strip() for x in r["threat_models_named"].split(";") if x.strip())
        interface = t & {"mitm", "replay", "reverse_pathway", "false_command"}
        model = t & {"poisoning", "evasion", "prompt"}
        return bool(interface or model), bool(interface), bool(model)

    # first verify the published counts on the full 83
    anyio = [r for r in full if interface_or_model(r)[0]]
    interf = [r for r in full if interface_or_model(r)[1]]
    model = [r for r in full if interface_or_model(r)[2]]
    both_im = [r for r in full if interface_or_model(r)[1] and interface_or_model(r)[2]]
    print(f"full 83: interface-union={len(interf)}, model-union={len(model)}, "
          f"overlap={len(both_im)}, either={len(anyio)} (paper says 56/44/27/15)")
    s_anyio = [r for r in strict if interface_or_model(r)[0]]
    s_ml = sum(1 for r in strict if r["ml_used"] == "yes")
    s_det = sum(1 for r in strict if r["ml_role"] == "detection")
    s_any = sum(1 for r in strict if r["ai_threat_overall"] in ("1", "2"))
    s_sub = sum(1 for r in strict if r["ai_threat_overall"] == "2")
    s_asn = sum(1 for r in strict if r["attack_surface_named"] == "yes")
    s_tool = sum(1 for r in strict if r["twin_role"] == "tool")
    s_unclear = sum(1 for r in strict if r["twin_role"] == "unclear")
    print(f"strict n={len(strict)}: ML={s_ml} ({s_ml/len(strict)*100:.1f}%), "
          f"detection={s_det} ({s_det/len(strict)*100:.1f}%), "
          f"any={s_any} ({s_any/len(strict)*100:.1f}%), "
          f"subst={s_sub} ({s_sub/len(strict)*100:.1f}%), "
          f"interface/model-threat naming={len(s_anyio)} "
          f"({len(s_anyio)/len(strict)*100:.1f}%), "
          f"attack_surface_named={s_asn}, tool={s_tool}, unclear={s_unclear}, target=0")
    sp = [r for r in strict if r["security_primary"] == "yes"
          and r["stance"] != "review" and r["ml_role"] == "detection"]
    sp_out = [r["id"] for r in sp if r["id"] in ("18", "69")]
    print(f"core subset n={len(sp)} after removing {sp_out}; "
          f"any={sum(1 for r in sp if r['ai_threat_overall'] in ('1','2'))}, "
          f"subst={sum(1 for r in sp if r['ai_threat_overall']=='2')}")
    # borderline-removed (R34, R68, R84) variant
    BORDER = {"34", "68", "84"}
    s2 = [r for r in full if r["id"] not in OUT_IDS | BORDER]
    s2_any = sum(1 for r in s2 if r["ai_threat_overall"] in ("1", "2"))
    s2_sub = sum(1 for r in s2 if r["ai_threat_overall"] == "2")
    s2_io = sum(1 for r in s2 if interface_or_model(r)[0])
    print(f"strict+borderline removed n={len(s2)}: any={s2_any} "
          f"({s2_any/len(s2)*100:.1f}%), subst={s2_sub} ({s2_sub/len(s2)*100:.1f}%), "
          f"io-naming={s2_io}")
    # what are the roles of the four out-of-scope records?
    for rid in sorted(OUT_IDS, key=int):
        r = next(x for x in full if x["id"] == rid)
        print(f"  R{rid}: role={r['twin_role']}, ai={r['ai_threat_overall']}, "
              f"io={interface_or_model(r)[0]}")

    # ---------------- Item 9: light quality appraisal ----------------
    print("\n=== Item 9: light quality appraisal ===")
    NON_PR_VENUES = {"30", "32", "65", "69"}  # Zenodo x2, GSC Online Press, IRJMETS
    out_rows = []
    for r in rows:
        ft = r["fulltext"] == "yes"
        cited = int(r["cited_by"] or 0) > 0
        peer = (r["id"] not in NON_PR_VENUES) and r["venue_type"] in (
            "journal", "conference", "book_chapter", "thesis")
        base = r["baseline_compared"] == "yes"
        metrics = r["metrics_reported"] == "yes"
        repro = (r["code_available"] == "yes") or (r["data_available"] == "yes")
        hiltb = r["eval_method"] in ("hardware-in-the-loop", "testbed")
        nonrev = r["stance"] != "review"
        signals = peer + cited + base + metrics + repro
        # 4-signal score for primary studies: peer, cited, comparative, repro
        primary_score = (peer + cited + (base or metrics) + repro) if (ft and nonrev) else ""
        out_rows.append({
            "id": r["id"], "fulltext": r["fulltext"], "stance": r["stance"],
            "venue_type": r["venue_type"], "peer_review_venue": "yes" if peer else "no",
            "cited": "yes" if cited else "no",
            "baseline_reported": "yes" if base else "no",
            "metrics_reported": "yes" if metrics else "no",
            "code_or_data_available": "yes" if repro else "no",
            "hil_or_testbed_eval": "yes" if hiltb else "no",
            "limitations_stated": r["limitations_stated"],
            "signals_0_5": signals,
            "primary_study_score_0_4": primary_score,
            "ai_threat_overall": r["ai_threat_overall"],
        })
    with open(os.path.join(AN, "quality_appraisal.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    prim = [r for r in out_rows if r["primary_study_score_0_4"] != ""]
    dist = Counter(int(r["primary_study_score_0_4"]) for r in prim)
    print(f"primary (non-review, full-text) studies n={len(prim)}; "
          f"4-signal score distribution (peer venue, cited, comparative eval, "
          f"code-or-data): {dict(sorted(dist.items()))}")
    for tier in (0, 1, 2, 3, 4):
        sub = [r for r in prim if int(r["primary_study_score_0_4"]) == tier]
        if not sub:
            continue
        any_ = sum(1 for r in sub if r["ai_threat_overall"] in ("1", "2"))
        sub_ = sum(1 for r in sub if r["ai_threat_overall"] == "2")
        print(f"  score {tier}: n={len(sub)} any={any_} ({any_/len(sub)*100:.0f}%) "
              f"subst={sub_} ({sub_/len(sub)*100:.0f}%)")
    hi = [r for r in prim if int(r["primary_study_score_0_4"]) >= 3]
    lo = [r for r in prim if int(r["primary_study_score_0_4"]) <= 1]
    if hi and lo:
        ha = sum(1 for r in hi if r["ai_threat_overall"] in ("1", "2"))
        la = sum(1 for r in lo if r["ai_threat_overall"] in ("1", "2"))
        hs = sum(1 for r in hi if r["ai_threat_overall"] == "2")
        ls = sum(1 for r in lo if r["ai_threat_overall"] == "2")
        print(f"  high (>=3): n={len(hi)}, any={ha/len(hi)*100:.0f}%, subst={hs/len(hi)*100:.0f}%")
        print(f"  low  (<=1): n={len(lo)}, any={la/len(lo)*100:.0f}%, subst={ls/len(lo)*100:.0f}%")
    # zero-citation count cross-check
    zc = sum(1 for r in rows if int(r["cited_by"] or 0) == 0)
    print(f"zero-citation records: {zc}/100")


if __name__ == "__main__":
    main()
