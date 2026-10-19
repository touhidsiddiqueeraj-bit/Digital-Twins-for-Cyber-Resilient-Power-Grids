#!/usr/bin/env python3
"""Build analysis/codes/adjudicated.txt — the reliability-sample adjudication.

Policy (recorded in the codebook): a disagreement is resolved to the value the
codebook + digest evidence dictate; where both values are defensible and the
evidence cannot separate them, C1 (the primary full-text coder) prevails and the
ambiguity is logged as a codebook revision. Multi-label `ml_family` is contracted
to the controlled vocabulary (its raw disagreement was mostly alias/format).
"""
import csv
import os

AN = os.path.join(os.path.dirname(os.path.abspath(__file__)))
FIELDS = ["id", "stance", "stance_confidence", "security_primary", "dt_type",
          "grid_domain", "twin_role", "attack_surface_named", "lifecycle_stage",
          "threat_models_named", "adversary_adaptive", "threat_model_explicit",
          "ml_used", "ml_role", "ml_family",
          "ai_threat_overall", "ai_adv_ml", "ai_evasion", "ai_poisoning", "ai_llm",
          "ai_agentic", "ai_threat_note",
          "eval_method", "testbed_or_dataset", "metrics_reported", "baseline_compared",
          "maturity", "limitations_stated", "code_available", "data_available",
          "notes"]

# Explicit adjudications (net change from C1), each with the deciding rule.
ADJ = {
    "22": {"stance": "bridge"},        # authors generate adversarial-ML data (build an attack) AND detect → §2.1
    "49": {"stance": "bridge", "dt_type": "process"},  # injects attacks AND defends; water-treatment SCADA process → §2.1/§3.1
    "62": {"grid_domain": "substation", "eval_method": "hil"},  # digital substations; HIL testbed → §3.2/§7
    "55": {"eval_method": "hil"},                      # HIL industrial testbed, not plain testbed/simulation → §7
    "2": {"threat_models_named": "fdi;other"},         # topology manipulation named → §4.1
    "43": {"threat_models_named": "fdi;dos;malware;poisoning;other"},  # "malicious software intrusion" named
}

# ml_family canonicalisation: alias -> controlled term
ALIAS = {
    "reinforcement": "RL", "rl": "RL", "drl": "RL", "ppo": "RL", "sac": "RL",
    "rnn": "RNN", "gru": "GRU", "lstm": "LSTM", "cnn": "CNN", "gnn": "GNN",
    "transformer": "transformer", "pinn": "PINN", "gan": "GAN",
    "svm": "SVM", "oc-svm": "SVM", "one-class-svm": "SVM", "one-class svm": "SVM",
    "if": "isolation-forest", "isolation forest": "isolation-forest",
    "isolation-forest": "isolation-forest", "lof": "LOF", "ee": "elliptic-envelope",
    "autoencoder": "autoencoder", "ae": "autoencoder", "vae": "autoencoder",
    "lstm-ae": "autoencoder", "ensemble": "ensemble", "ensemble deep learning": "ensemble",
    "federated": "federated", "federated learning": "federated",
    "rf": "RF", "random forest": "RF", "xgboost": "XGBoost", "knn": "kNN", "dnn": "DNN",
    "ml": "ML", "dl": "DL", "nn": "NN", "ann": "NN", "neural network": "NN",
    "artificial neural networks": "NN", "machine learning": "ML", "deep learning": "DL",
    "machine learning general": "ML", "hmm": "HMM", "hidden markov model": "HMM",
}


def canon_family(a, b):
    out = []
    for src in (a, b):
        for tok in src.replace(",", ";").split(";"):
            t = tok.strip().lower()
            t = t.split("(")[0].strip()          # "rl (ppo/sac)" -> "rl"
            if not t:
                continue
            c = ALIAS.get(t, tok.strip())
            if c not in out:
                out.append(c)
    return ";".join(out)


def main():
    c1 = {r["id"]: r for r in csv.DictReader(open(os.path.join(AN, "coder1_codes.csv"), encoding="utf-8"))}
    c2 = {r["id"]: r for r in csv.DictReader(open(os.path.join(AN, "reliability", "coder2_sheet.csv"), encoding="utf-8"))}
    ids = [r["id"] for r in csv.DictReader(open(os.path.join(AN, "reliability", "sample20.csv"), encoding="utf-8"))]

    lines = ["# Adjudicated codes for the 20-paper reliability sample (delimiter @@).",
             "# Fields equal to C1 are as C1; ml_family is the canonical union of C1+C2.",
             "# " + "@@".join(FIELDS)]
    for i in ids:
        row = {k: c1[i][k] for k in FIELDS}
        row["ml_family"] = canon_family(c1[i]["ml_family"], c2[i]["ml_family"])
        for k, v in ADJ.get(i, {}).items():
            row[k] = v
        lines.append("@@".join(row[k] for k in FIELDS))

    out = os.path.join(AN, "codes", "adjudicated.txt")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {out}: {len(ids)} rows")


if __name__ == "__main__":
    main()
