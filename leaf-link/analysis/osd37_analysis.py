"""
LEAF-Link analysis of NASA OSDR study OSD-37 (Arabidopsis thaliana, spaceflight vs ground control).

Independent research by Arjun, Null Set Labs. Principal component analysis written April 2026;
the held-out classification, permutation test and technical checks were added in October 2026
when the study was closed out.

Data (public, not redistributed here): https://osdr.nasa.gov/bio/repo/data/studies/OSD-37
  GLDS-37_rna_seq_Normalized_Counts_rRNArm_GLbulkRNAseq.csv   (GeneLab normalized counts)
  s_OSD-37.txt                                                 (ISA sample table)
  a_OSD-37_transcription-profiling_rna-sequencing-(rna-seq)_Illumina.txt  (ISA assay table)

Usage:
  python osd37_analysis.py path/to/OSD-37 [--permutations 200]
Writes results/osd37_results.json next to this script.
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

N_TOP = 5000          # most variable genes kept after log2(x + 1)
SEED = 204


def load(data_dir):
    counts = pd.read_csv(data_dir / "GLDS-37_rna_seq_Normalized_Counts_rRNArm_GLbulkRNAseq.csv", index_col=0)
    meta = pd.read_csv(data_dir / "s_OSD-37.txt", sep="\t").set_index("Sample Name")
    common = [s for s in counts.columns if s in meta.index]
    counts, meta = counts[common], meta.loc[common]
    return counts, meta


def top_var_scaled(log_samples_by_genes, n=N_TOP):
    idx = np.argsort(log_samples_by_genes.var(axis=0))[-n:]
    return StandardScaler().fit_transform(log_samples_by_genes[:, idx])


def eta2(scores, groups):
    """Share of a component's variance explained by a grouping (one-way ANOVA eta squared)."""
    grand = scores.mean()
    total = ((scores - grand) ** 2).sum()
    between = sum(((scores[groups == g].mean() - grand) ** 2) * (groups == g).sum() for g in np.unique(groups))
    return float(between / total)


class TopVar(BaseEstimator, TransformerMixin):
    """Keep the n most variable genes, chosen on the training fold only."""
    def __init__(self, n=N_TOP):
        self.n = n

    def fit(self, X, y=None):
        self.idx_ = np.argsort(X.var(axis=0))[-self.n:]
        return self

    def transform(self, X):
        return X[:, self.idx_]


def classifier():
    return make_pipeline(TopVar(), StandardScaler(), LogisticRegression(max_iter=5000, C=0.1))


def held_out_accuracy(L, y, groups):
    """Leave one group out: both samples from a canister position are held out together."""
    pred = np.zeros_like(y)
    for g in np.unique(groups):
        test = groups == g
        pred[test] = classifier().fit(L[~test], y[~test]).predict(L[test])
    return float((pred == y).mean()), pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir", type=Path)
    ap.add_argument("--permutations", type=int, default=200)
    args = ap.parse_args()

    counts, meta = load(args.data_dir)
    names = np.array(counts.columns)
    cond = meta["Factor Value[Spaceflight]"].astype(str).values
    eco = meta["Factor Value[Ecotype]"].astype(str).values
    rnd = np.array([re.search(r"_(R[12])-", n).group(1) for n in names])
    pos = np.array([re.search(r"-((?:FL|GC)-[A-D]\d)$", n).group(1) for n in names])
    L = np.log2(counts.values.astype(float).T + 1.0)  # samples x genes

    out = {"study": "OSD-37", "n_genes": int(counts.shape[0]), "n_samples": int(len(names)),
           "condition_counts": pd.Series(cond).value_counts().to_dict(),
           "ecotype_counts": pd.Series(eco).value_counts().to_dict()}

    # 1. PCA on all samples
    X = top_var_scaled(L)
    pca = PCA(n_components=6).fit(X)
    Z = pca.transform(X)
    out["variance_explained_pct"] = [round(float(v) * 100, 2) for v in pca.explained_variance_ratio_]
    out["eta2"] = {f"PC{i + 1}": {"ecotype": round(eta2(Z[:, i], eco), 3),
                                  "spaceflight": round(eta2(Z[:, i], cond), 3),
                                  "round_R1_R2": round(eta2(Z[:, i], rnd), 3)} for i in range(6)}
    out["points"] = [{"sample": names[i], "pc1": round(float(Z[i, 0]), 2), "pc2": round(float(Z[i, 1]), 2),
                      "condition": cond[i], "ecotype": eco[i]} for i in range(len(names))]

    # 2. PCA within each ecotype
    out["within_ecotype"] = {}
    for e in sorted(np.unique(eco)):
        m = eco == e
        pe = PCA(n_components=3).fit(top_var_scaled(L[m]))
        Ze = pe.transform(top_var_scaled(L[m]))
        out["within_ecotype"][e] = {
            "n": int(m.sum()),
            "variance_explained_pct": [round(float(v) * 100, 1) for v in pe.explained_variance_ratio_],
            "eta2_spaceflight": [round(eta2(Ze[:, i], cond[m]), 3) for i in range(3)],
            "points": [{"pc1": round(float(Ze[i, 0]), 2), "pc2": round(float(Ze[i, 1]), 2), "condition": cond[m][i]}
                       for i in range(int(m.sum()))]}

    # 3. Flight vs ground from expression alone, holding out canister positions
    y = (cond == "Space Flight").astype(int)
    acc, pred = held_out_accuracy(L, y, pos)
    out["classification"] = {"model": "L2 logistic regression (C=0.1) on the 5,000 most variable genes, "
                                      "gene filter and scaling fitted inside each training fold",
                             "cv": "leave one canister position out (28 folds, 2 samples each)",
                             "accuracy": round(acc, 4), "correct": int((pred == y).sum()),
                             "misclassified": names[pred != y].tolist(),
                             "per_ecotype_accuracy": {e: round(float((pred[eco == e] == y[eco == e]).mean()), 3)
                                                      for e in np.unique(eco)}}

    # 4. Permutation test: shuffle flight/ground between canister positions within each ecotype
    rng = np.random.default_rng(SEED)
    pos_ids = np.unique(pos)
    pos_label = {p: y[pos == p][0] for p in pos_ids}
    pos_eco = {p: eco[pos == p][0] for p in pos_ids}
    null = []
    for _ in range(args.permutations):
        relabel = {}
        for e in np.unique(eco):
            ps = [p for p in pos_ids if pos_eco[p] == e]
            relabel.update(zip(ps, rng.permutation([pos_label[p] for p in ps])))
        null.append(held_out_accuracy(L, np.array([relabel[p] for p in pos]), pos)[0])
    null = np.array(null)
    out["permutation"] = {"n": args.permutations, "null_mean": round(float(null.mean()), 3),
                          "null_95th": round(float(np.percentile(null, 95)), 3), "null_max": round(float(null.max()), 3),
                          "p": round(float((1 + (null >= acc).sum()) / (args.permutations + 1)), 4)}

    # 5. Technical checks from the ISA assay table
    assay = pd.read_csv(args.data_dir / "a_OSD-37_transcription-profiling_rna-sequencing-(rna-seq)_Illumina.txt",
                        sep="\t").set_index("Sample Name").loc[names]
    tech = {}
    for col, key in (("Parameter Value[Read Depth]", "read_depth_mean"),
                     ("Parameter Value[rRNA Contamination]", "rrna_pct_mean")):
        v = pd.to_numeric(assay[col], errors="coerce").values
        tech[key] = {c: round(float(np.nanmean(v[cond == c])), 2) for c in np.unique(cond)}
    tech["read_length_counts"] = assay["Parameter Value[Read Length]"].astype(str).value_counts().to_dict()
    out["technical"] = tech

    dest = Path(__file__).parent / "results" / "osd37_results.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("variance_explained_pct", "eta2", "classification", "permutation", "technical")}, indent=1))


if __name__ == "__main__":
    main()
