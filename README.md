# Quantum Cryptography (BB84 and B92)

This GitHub repository contains the code and data for the quantum key
distribution (QKD) experiments performed by Felipe Tcach and Charlie Perkins
during the Semester 5 Laboratory period (2023).

## About this repository

This repo has been branched from the original repository that was used to run
the experiment. The original repo holds the working state at the time of the
lab submission. This branch exists to clean up and reorganise the source code,
data, and results without disturbing that historical record.

## Experimental aims

The aim of the experiment was to explore the fidelity of information transfer 
for the QKD protocols BB84 and B92.

## Results and reasoning

Important results can be found in the [results/](results/) folder at the
repository root. Measurements of the ratios of polarised laser light were
taken on an oscilloscope and analysed using Python (see [source/](source/)).
The ratios of the intensities can be treated as the approximate single-photon
probabilities of detection. These values are then used to simulate large-scale
key distribution many times over, giving statistical insight into the QKD
protocols.

## Probability normalisation

The raw probabilities in [source/qkd/constants.py](source/qkd/constants.py)
are measured detection ratios for each of the 8 possible qubit/basis
combinations (e.g. `1AB`, `0BB`). Because the two outcomes for any given
basis pairing (e.g. `0AA` and `1AA`) were measured independently rather than
as a constrained pair, they do not necessarily sum to 1. Before the Monte
Carlo simulation runs, `renormalise_probabilities` in
[source/qkd/utils.py](source/qkd/utils.py) rescales each matched pair so
that they sum to 1, and propagates the uncertainties accordingly. The
simulation therefore works with self-consistent conditional probabilities,
while the raw experimental values in `constants.py` are preserved unchanged.

## Repository layout

```
quantum-cryptography/
├── Makefile                         # simulate-then-plot pipeline for B92 and BB84
├── requirements.txt
├── data/
│   ├── b92_data/                    # CSV output from b92_sim.py
│   └── bb84_data/                   # CSV output from bb84_sim.py
├── results/                         # PDF figures used in the report
└── source/
    ├── qkd/                         # shared package (import as qkd.*)
    │   ├── constants.py             # probability dicts, N, REPEATS, B92_STATE_ORDER
    │   └── utils.py                 # generate_bits, check_keys, pack_probabilities
    ├── simulations/
    │   ├── b92_sim.py               # B92 Monte Carlo, writes to data/b92_data/
    │   └── bb84_sim.py              # BB84 Monte Carlo, writes to data/bb84_data/
    └── plotting/
        ├── fidelity_graph.py        # reads simulation CSVs for either protocol
        └── photon_probability.py    # bar chart of raw photon probabilities
```

## Running the pipeline

A Makefile at the repository root coordinates the full simulate-then-plot
workflow for both the B92 and BB84 protocols across both error regimes. It
reads `N` and `REPEATS` directly from `constants.py` so output filenames
always stay in sync.

```
make all         # simulate + plot for both protocols and both regimes (default)
make simulate    # run B92 and BB84 Monte Carlo for both regimes
make plot        # plot results for both regimes (requires CSVs from simulate)
make clean       # remove generated CSVs and PDFs
make help        # list all targets
```

Per-protocol and per-regime targets are also available:

```
make simulate-b92 / simulate-bb84
make simulate-b92-low / simulate-b92-high
make simulate-bb84-low / simulate-bb84-high
make plot-b92 / plot-bb84
make plot-b92-low / plot-b92-high
make plot-bb84-low / plot-bb84-high
```

Scripts can also be run directly from the `source/` directory:

```
cd source
python -m simulations.b92_sim --regime low
python -m simulations.bb84_sim --regime high
python -m plotting.fidelity_graph --protocol b92 --regime low
python -m plotting.fidelity_graph --protocol bb84 --regime high
python -m plotting.photon_probability --regime high
```

## Requirements

Python dependencies are listed in [requirements.txt](requirements.txt).
Install with:

```
pip install -r requirements.txt
```

A `.venv/` is present at the repo root. The Makefile uses `.venv/bin/python`
automatically.
