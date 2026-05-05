# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Python code and data for a 2023 lab project on the BB84 and B92 quantum key distribution (QKD) protocols. The active branch is reorganising and consolidating the original lab submission without altering its scientific content.

## Running the pipeline

The Makefile is the primary way to run the full simulate-then-plot pipeline for both protocols and both error regimes:

```
make all             # simulate + plot for B92 and BB84, low and high regimes (default)
make simulate        # run B92 and BB84 simulations for both regimes
make plot            # plot B92 and BB84 results for both regimes
make clean           # remove generated CSVs and PDFs
make help            # list all targets
```

Per-protocol and per-regime targets exist for both stages:

```
make simulate-b92 / simulate-bb84
make simulate-b92-low / simulate-b92-high / simulate-bb84-low / simulate-bb84-high
make plot-b92 / plot-bb84
make plot-b92-low / plot-b92-high / plot-bb84-low / plot-bb84-high
```

The Makefile reads `N` and `REPEATS` directly from `constants.py` so filenames stay in sync automatically. It uses `.venv/bin/python` and sets `PYTHONPATH=source`.

Individual scripts can also be run directly from the `source/` directory:

```
cd source
python -m simulations.b92_sim --regime low
python -m simulations.bb84_sim --regime high
python -m plotting.fidelity_graph --protocol b92 --regime low
python -m plotting.fidelity_graph --protocol bb84 --regime high
python -m plotting.photon_probability --regime high
```

Both simulation scripts accept `--regime {low,high}`. `fidelity_graph.py` accepts `--protocol {b92,bb84}` and `--regime {low,high}`. `photon_probability.py` accepts `--regime {low,high}`.

## Setup

```
pip install -r requirements.txt
```

A `.venv/` is already present at the repo root.

## Architecture

The code separates three concerns:

- **[source/qkd/constants.py](source/qkd/constants.py)** is the single source of truth for simulation inputs. It defines `PROBABILITIES_LOW` and `PROBABILITIES_HIGH` as dicts keyed by 8 qubit/basis/measurement combinations (`'0AA'`, `'0AB'`, ..., `'1BB'`), each mapping to `(probability, uncertainty)`. It also defines `N` (Alice's starting key length), `REPEATS` (Monte Carlo repeats), and `B92_STATE_ORDER` (the 4 B92 states in case-index order). The header docstring documents the `<bit><tx_basis><rx_basis>` key convention and is the authoritative reference for what each state means.
- **[source/qkd/utils.py](source/qkd/utils.py)** holds protocol-agnostic helpers: `generate_bits`, `check_keys`, `renormalise_probabilities` (combines matched basis pairs so probabilities sum to 1), and `pack_probabilities` (calls `renormalise_probabilities` then packs the 4 B92 states into two float arrays indexed by `case = 2*alice_basis + bob_basis`).
- **[source/simulations/](source/simulations/)** contains the Monte Carlo drivers: `b92_sim.py` and `bb84_sim.py`. Each script generates random keys/bases, looks up per-state probabilities from `constants.py`, draws a normally distributed sample around `(prob, uncertainty)` for each bit, and compares Alice's key to Bob's reconstructed key. They write CSVs to `data/b92_data/` and `data/bb84_data/` respectively, at the repo root.
- **[source/plotting/](source/plotting/)** contains the plotting scripts. `fidelity_graph.py` reads the simulation CSVs for either protocol (selected by `--protocol`) and produces fidelity PDFs. `photon_probability.py` reads directly from `constants.py` and produces the photon-probability bar charts. Both write PDFs to `results/` at the repo root.

The probability values in `constants.py` are derived from real oscilloscope measurements of polarised laser intensity ratios; the simulations treat those ratios as single-photon detection probabilities. If `constants.py` values change, all simulations and plots downstream should be regenerated (`make clean && make all`).

## Writing style for docs/comments in this repo

Per the user's global instructions: no em dashes, and avoid the words "delve", "nuance", "genuine", "first-hand", "hands on", "leverage", "tapestry", "comprehensive", "testament", "crucial", "pivotal", "intricate", "underscore" in any prose written into this repo (READMEs, docstrings, commit messages).
