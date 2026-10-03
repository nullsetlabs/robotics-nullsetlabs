"""
LEAF-Link robustness checks on NASA OSDR study OSD-37 (added October 2026 at close-out).

1. Transfer across strains: train flight-vs-ground on three strains, test on the fourth.
2. Sensitivity: number of variable genes kept and regularization strength.
3. Permutation test with 1,000 shuffles for the main model.
4. Known biology: heat-shock genes and class III peroxidases, which the original study
   (Choi et al. 2019, doi:10.1002/ajb2.1223) reported as up and down in spaceflight.
   Gene identities are from UniProt reviewed entries (see results file).

Usage: python osd37_robustness.py path/to/OSD-37 [--permutations 1000]
Writes results/osd37_robustness.json next to this script.
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from osd37_analysis import TopVar, eta2, load, top_var_scaled

SEED = 204

# Heat-shock genes, AGI locus -> UniProt name (reviewed entries, checked October 2026)
HSP = {"AT1G74310": "HSP101", "AT5G52640": "HSP90-1", "AT5G56010": "HSP90-3", "AT3G12580": "HSP70-4",
       "AT1G16030": "HSP70-5", "AT4G27670": "HSP21", "AT5G12020": "HSP17.6II", "AT5G12030": "HSP17.7",
       "AT1G53540": "HSP17.6C", "AT2G29500": "HSP17.6B", "AT3G46230": "HSP17.4A", "AT5G59720": "HSP18.1",
       "AT4G21320": "HSA32", "AT2G26150": "HSFA2"}


def model(n_top=5000, C=0.1):
    return make_pipeline(TopVar(n_top), StandardScaler(), LogisticRegression(max_iter=5000, C=C))


def grouped_accuracy(L, y, groups, n_top=5000, C=0.1):
    pred = np.zeros_like(y)
    for g in np.unique(groups):
        te = groups == g
        pred[te] = model(n_top, C).fit(L[~te], y[~te]).predict(L[te])
    return float((pred == y).mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir", type=Path)
    ap.add_argument("--permutations", type=int, default=1000)
    ap.add_argument("--peroxidases", type=Path, default=Path(__file__).parent / "results" / "uniprot_class3_peroxidases.tsv")
    args = ap.parse_args()

    counts, meta = load(args.data_dir)
    names = np.array(counts.columns)
    cond = meta["Factor Value[Spaceflight]"].astype(str).values
    eco = meta["Factor Value[Ecotype]"].astype(str).values
    pos = np.array([re.search(r"-((?:FL|GC)-[A-D]\d)$", n).group(1) for n in names])
    L = np.log2(counts.values.astype(float).T + 1.0)
    y = (cond == "Space Flight").astype(int)
    out = {}

    # 1. Leave one strain out
    lso = {}
    for e in np.unique(eco):
        te = eco == e
        m = model().fit(L[~te], y[~te])
        lso[e] = {"n": int(te.sum()), "accuracy": round(float((m.predict(L[te]) == y[te]).mean()), 3),
                  "mean_prob_flight_for_flight": round(float(m.predict_proba(L[te & (y == 1)])[:, 1].mean()), 3),
                  "mean_prob_flight_for_ground": round(float(m.predict_proba(L[te & (y == 0)])[:, 1].mean()), 3)}
    out["leave_one_strain_out"] = lso

    # 2. Sensitivity of the PCA result and the held-out accuracy
    expressed = (counts.values.mean(axis=1) >= 10)
    sens = []
    for n_top in (1000, 2000, 5000, 10000, int(expressed.sum())):
        X = top_var_scaled(L, n_top)
        Z = PCA(n_components=6).fit_transform(X)
        row = {"genes": n_top,
               "strain_share_pc1": round(eta2(Z[:, 0], eco), 3), "strain_share_pc2": round(eta2(Z[:, 1], eco), 3),
               "max_spaceflight_share_pc1_6": round(max(eta2(Z[:, i], cond) for i in range(6)), 3),
               "accuracy_C0.1": round(grouped_accuracy(L, y, pos, n_top, 0.1), 3)}
        sens.append(row)
    out["sensitivity_genes"] = sens
    out["expressed_gene_rule"] = "mean normalized count >= 10 across all samples"
    out["sensitivity_C"] = {str(C): round(grouped_accuracy(L, y, pos, 5000, C), 3) for C in (0.01, 0.1, 1.0)}

    # 3. Permutation test, 1,000 shuffles of flight/ground between canister positions within each strain
    acc = grouped_accuracy(L, y, pos)
    rng = np.random.default_rng(SEED)
    pos_ids = np.unique(pos)
    lab = {p: y[pos == p][0] for p in pos_ids}
    peco = {p: eco[pos == p][0] for p in pos_ids}
    null = []
    for _ in range(args.permutations):
        new = {}
        for e in np.unique(eco):
            ps = [p for p in pos_ids if peco[p] == e]
            new.update(zip(ps, rng.permutation([lab[p] for p in ps])))
        null.append(grouped_accuracy(L, np.array([new[p] for p in pos]), pos))
    if args.permutations > 0:
        null = np.array(null)
        out["permutation"] = {"n": args.permutations, "observed": round(acc, 4), "null_mean": round(float(null.mean()), 3),
                              "null_95th": round(float(np.percentile(null, 95)), 3), "null_max": round(float(null.max()), 3),
                              "n_null_at_or_above_observed": int((null >= acc).sum()),
                              "p": round(float((1 + (null >= acc).sum()) / (args.permutations + 1)), 4)}

    # 4. Known biology: direction of change in flight within each strain (difference of mean log2 counts)
    def lfc(gene_ids):
        res = {}
        for e in np.unique(eco):
            f = (eco == e) & (y == 1)
            g = (eco == e) & (y == 0)
            idx = [counts.index.get_loc(a) for a in gene_ids if a in counts.index]
            res[e] = (L[f][:, idx].mean(axis=0) - L[g][:, idx].mean(axis=0))
        return res

    hsp_ids = [a for a in HSP if a in counts.index]
    h = lfc(hsp_ids)
    out["heat_shock"] = {"genes": {a: HSP[a] for a in hsp_ids},
                         "log2_fold_change": {e: {HSP[a]: round(float(v), 2) for a, v in zip(hsp_ids, h[e])} for e in h},
                         "n_up_per_strain": {e: int((h[e] > 0).sum()) for e in h},
                         "n_up_in_all_four": int(np.all(np.vstack([h[e] > 0 for e in h]), axis=0).sum()),
                         "n_genes": len(hsp_ids)}

    prx = pd.read_csv(args.peroxidases, sep="\t")
    prx = prx[prx["Protein families"].astype(str).str.contains("class III")]
    prx_ids = sorted({str(x).split()[0].upper() for x in prx["Gene Names (ordered locus)"].dropna()})
    expressed_ids = set(counts.index[expressed])
    prx_ids = [a for a in prx_ids if a in expressed_ids]
    prx_name = {str(r["Gene Names (ordered locus)"]).split()[0].upper(): str(r["Gene Names (primary)"])
                for _, r in prx.iterrows()}
    pr = lfc(prx_ids)
    all_expr = lfc(sorted(expressed_ids))
    out["peroxidases"] = {"log2_fold_change": {e: {prx_name.get(a, a): round(float(v), 2) for a, v in zip(prx_ids, pr[e])} for e in pr},
                          "n_class3_expressed": len(prx_ids),
                          "fraction_down_per_strain": {e: round(float((pr[e] < 0).mean()), 3) for e in pr},
                          "median_log2_fc_per_strain": {e: round(float(np.median(pr[e])), 3) for e in pr},
                          "all_expressed_genes_fraction_down": {e: round(float((all_expr[e] < 0).mean()), 3) for e in all_expr},
                          "n_expressed_genes": len(expressed_ids)}

    dest = Path(__file__).parent / "results" / "osd37_robustness.json"
    dest.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
