# LEAF-Link analysis

Code and results behind the LEAF-Link concept study at `robotics.nullsetlabs.org/leaf-link/`. Independent research by Arjun, Null Set Labs, 2026.

## Files

| File | What it does |
|---|---|
| `osd37_analysis.py` | Principal component analysis of NASA OSDR study OSD-37, share of each component explained by strain and by spaceflight, analysis within each strain, held-out classification of flight versus ground, permutation test, and technical checks. |
| `chamber_pid_sim.py` | One temperature channel of a plant growth chamber under PID control: a 20 to 25 C setpoint step and three gain sets. |
| `results/osd37_results.json` | Output of `osd37_analysis.py` (200 permutations). |
| `results/pid_results.json` | Output of `chamber_pid_sim.py`. |

## Data

OSD-37 is public at https://osdr.nasa.gov/bio/repo/data/studies/OSD-37 and is not copied here. Download these three files from the study's Files tab into one folder:

- `GLDS-37_rna_seq_Normalized_Counts_rRNArm_GLbulkRNAseq.csv`
- `s_OSD-37.txt` (in the ISA metadata archive)
- `a_OSD-37_transcription-profiling_rna-sequencing-(rna-seq)_Illumina.txt` (in the ISA metadata archive)

## Run

Python 3 with numpy, pandas and scikit-learn.

```
python osd37_analysis.py path/to/OSD-37 --permutations 200
python chamber_pid_sim.py
```

The permutation test refits the classifier 28 times per permutation and takes several minutes. Random seed 204.

## History

The principal component analysis and the control simulation were written in April 2026. The held-out classification, permutation test and technical checks were added in October 2026, when the study was closed out; the control simulation's model and gains are unchanged.
