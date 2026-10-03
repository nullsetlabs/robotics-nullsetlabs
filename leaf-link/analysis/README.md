# LEAF-Link analysis

Code and results behind the LEAF-Link concept study at `robotics.nullsetlabs.org/leaf-link/`. Independent research by Arjun, Null Set Labs, 2026.

## Files

| File | What it does |
|---|---|
| `osd37_analysis.py` | Principal component analysis of NASA OSDR study OSD-37, share of each component explained by strain and by spaceflight, analysis within each strain, held-out classification of flight versus ground, permutation test, and technical checks. |
| `osd37_robustness.py` | Transfer across strains (train on three, test on the fourth), sensitivity to the number of genes kept and to regularization, a 1,000-shuffle permutation test, and the direction of change in flight for heat-shock genes and class III peroxidases. |
| `chamber_pid_sim.py` | One temperature channel of a plant growth chamber under PID control: a 20 to 25 C setpoint step, three gain sets, and a sweep of sensor dead time from 0 to 120 s. |
| `results/osd37_results.json` | Output of `osd37_analysis.py` (200 permutations). |
| `results/osd37_robustness.json` | Output of `osd37_robustness.py` (1,000 permutations). |
| `results/pid_results.json` | Output of `chamber_pid_sim.py`. |
| `results/uniprot_class3_peroxidases.tsv` | Arabidopsis peroxidases from UniProt reviewed entries (query run October 3, 2026), used to identify the class III peroxidases. The heat-shock genes are listed in `osd37_robustness.py`. |

## Data

OSD-37 is public at https://osdr.nasa.gov/bio/repo/data/studies/OSD-37 and is not copied here. Download these three files from the study's Files tab into one folder:

- `GLDS-37_rna_seq_Normalized_Counts_rRNArm_GLbulkRNAseq.csv`
- `s_OSD-37.txt` (in the ISA metadata archive)
- `a_OSD-37_transcription-profiling_rna-sequencing-(rna-seq)_Illumina.txt` (in the ISA metadata archive)

## Run

Python 3 with numpy, pandas and scikit-learn.

```
python osd37_analysis.py path/to/OSD-37 --permutations 200
python osd37_robustness.py path/to/OSD-37 --permutations 1000
python chamber_pid_sim.py
```

Each permutation refits the classifier 28 times; 1,000 permutations take about 15 minutes on a laptop. Random seed 204.

## History

The principal component analysis and the control simulation were written in April 2026. The held-out classification, permutation tests, transfer and sensitivity checks, known-gene check, technical checks and the sensor dead-time sweep were added in October 2026, when the study was closed out; the control simulation's model and gains are unchanged.
