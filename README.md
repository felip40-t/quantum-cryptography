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

## Repository layout

- [source/qkd/](source/qkd/) — shared utilities ([utils.py](source/qkd/utils.py))
  and probability constants ([constants.py](source/qkd/constants.py)) for the
  high- and low-error regimes.
- [source/simulations/](source/simulations/) — Monte Carlo simulations for
  BB84 ([bb84_fidelity.py](source/simulations/bb84_fidelity.py)) and B92
  ([b92_sim1.py](source/simulations/b92_sim1.py),
  [b92_sim2.py](source/simulations/b92_sim2.py),
  [b92_sim3.py](source/simulations/b92_sim3.py)).
- [source/plotting/](source/plotting/) — plotting scripts, including
  [photon_probability.py](source/plotting/photon_probability.py) which
  produces the photon-probability bar charts for both error regimes via CLI
  flags.
- [data/](data/) — raw and processed oscilloscope datasets.
- [results/](results/) — final plots used in the report.

## Planned changes

The files [b92_sim1.py](source/simulations/b92_sim1.py),
[b92_sim2.py](source/simulations/b92_sim2.py), and
[b92_sim3.py](source/simulations/b92_sim3.py) will be merged into a single
`b92_sim.py` file. The aim is to mirror the BB84 layout, with one simulation
script per protocol that reads its parameters from
[constants.py](source/qkd/constants.py).

## Requirements

Python dependencies are listed in [requirements.txt](requirements.txt).
Install with:

```
pip install -r requirements.txt
```
