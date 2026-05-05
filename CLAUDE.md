# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Python code and data for a 2023 lab project on the BB84 and B92 quantum key distribution (QKD) protocols. The active branch (`cleanup`) is reorganising and consolidating the original lab submission without altering its scientific content.

## Running the pipeline

The Makefile is the primary way to run the full B92 simulate-then-plot pipeline:

```
make simulate    # run B92 Monte Carlo for both regimes
make plot        # plot results for both regimes (requires CSVs from simulate)
make all         # simulate + plot (default target)
make clean       # remove generated CSVs and PDFs
make help        # list all targets
```

The Makefile reads `N` and `REPEATS` directly from `constants.py` so filenames stay in sync automatically. It uses `.venv/bin/python` and sets `PYTHONPATH=source`.

Individual scripts can also be run directly from the `source/` directory:

```
cd source
python -m simulations.b92_sim --regime low
python -m plotting.b92_graph --regime high
python -m plotting.photon_probability --regime high
```

`b92_sim.py`, `b92_graph.py`, and `photon_probability.py` all accept `--regime {low,high}`.

## Setup

```
pip install -r requirements.txt
```

A `.venv/` is already present at the repo root.

## Architecture

The code separates three concerns:

- **[source/qkd/constants.py](source/qkd/constants.py)** — the single source of truth for simulation inputs. Defines `PROBABILITIES_LOW` and `PROBABILITIES_HIGH` as dicts keyed by 8 qubit/basis/measurement combinations (`'0AA'`, `'0AB'`, ..., `'1BB'`), each mapping to `(probability, uncertainty)`. Also defines `N` (Alice's starting key length), `REPEATS` (Monte Carlo repeats), and `B92_STATE_ORDER` (the 4 B92 states in case-index order). The header docstring documents the `<bit><tx_basis><rx_basis>` key convention and is the authoritative reference for what each state means.
- **[source/qkd/utils.py](source/qkd/utils.py)** — protocol-agnostic helpers: `generate_bits`, `check_keys`, `renormalise_probabilities` (combines matched basis pairs so probabilities sum to 1), `pack_probabilities` (calls `renormalise_probabilities` then packs the 4 B92 states into two float arrays indexed by `case = 2*alice_basis + bob_basis`).
- **[source/simulations/](source/simulations/)** — Monte Carlo drivers. Each script generates random keys/bases, looks up per-state probabilities from `constants.py`, draws a normally distributed sample around `(prob, uncertainty)` for each bit, and compares Alice's key to Bob's reconstructed key. Writes CSVs to `data/b92_data/` at the repo root.
- **[source/plotting/](source/plotting/)** — plotting scripts. `b92_graph.py` reads the simulation CSVs and produces fidelity PDFs. `photon_probability.py` reads directly from `constants.py` and produces the photon-probability bar charts. Both write PDFs to `results/` at the repo root.

The probability values in `constants.py` are derived from real oscilloscope measurements of polarised laser intensity ratios; the simulations treat those ratios as single-photon detection probabilities. If `constants.py` values change, all simulations and plots downstream should be regenerated.

## `bb84_fidelity.py` status

[source/simulations/bb84_fidelity.py](source/simulations/bb84_fidelity.py) is not yet cleaned up. It references a `PROBABILITIES` tuple (not the dict in `constants.py`) inside `run_experiment`, has a `SIMULATE` flag switching between live simulation and a hardcoded CSV path, and writes its figure to `..//results//Fidelity_16.png`. Its title and CSV filename both say "B92" despite the file being named `bb84_fidelity.py`. Expect to refactor it to mirror the structure of `b92_sim.py` before relying on its output.

## Writing style for docs/comments in this repo

Per the user's global instructions: no em dashes, and avoid the words "delve", "nuance", "genuine", "first-hand", "hands on", "leverage", "tapestry", "comprehensive", "testament", "crucial", "pivotal", "intricate", "underscore" in any prose written into this repo (READMEs, docstrings, commit messages).
