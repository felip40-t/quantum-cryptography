"""
Simulate the B92 protocol for different error regimes and save the data.

"""

import argparse
import time

import numpy as np
import pandas as pd

from pathlib import Path
from qkd.constants import RUNS, N, PROBABILITIES_LOW, PROBABILITIES_HIGH, B92_STATE_ORDER
from qkd.utils import generate_bits, check_keys, pack_probabilities, save_data

def results(alice_basis: np.ndarray, bob_basis: np.ndarray, probs_arr: np.ndarray, errs_arr: np.ndarray):
    """
    Vectorised Monte Carlo step. For each bit, draws a per-observation
    probability sample around (prob, error), compares against a uniform draw
    to decide whether Bob's measurement is the on-axis (omitted) outcome or
    the off-axis (kept) outcome.

    Returns Bob's reconstructed key and a boolean mask marking which input
    bits were kept (used to filter Alice's key in step with Bob).
    """
    # Map (alice_basis, bob_basis) pairs to case indices for probability lookup.
    case = 2 * alice_basis.astype(np.int64) + bob_basis.astype(np.int64)
    # Generate sample probabilities for each bit based on case-specific mean and error.
    sampled_p = np.random.normal(probs_arr[case], errs_arr[case])
    # Clip probabilities to [0, 1] to ensure valid comparisons.
    np.clip(sampled_p, 0.0, 1.0, out=sampled_p)
    rand_vals = np.random.random(case.shape[0])
    # Boolean mask for which bits are kept: Bob's measurement is kept if the random
    # value is greater than or equal to the sampled probability. Check README for details.
    kept = rand_vals >= sampled_p
    # Bob's key bit is the opposite of his basis for kept bits.
    bob_key = (1 - bob_basis[kept]).astype(np.int8)
    return bob_key, kept

def main():
    parser = argparse.ArgumentParser(description=
        'Simulate the B92 protocol for different error regimes and save the data.'
    )
    parser.add_argument(
        "--regime",
        choices=["low", "high"],
        default="low",
        help="Error regime to use for probabilities and uncertainties (default: low).",
    )
    parser.add_argument(
        "--norm",
        action="store_true",
        help="Renormalise probabilities to ensure valid distributions (default: False).",
    )
    
    args = parser.parse_args()

    start = time.perf_counter()

    if args.regime == "high":
        probs_arr, errs_arr = pack_probabilities(PROBABILITIES_HIGH, norm=args.norm)
    else:
        probs_arr, errs_arr = pack_probabilities(PROBABILITIES_LOW, norm=args.norm)

    initial_lengths = np.tile(np.arange(32, N, 4), RUNS)
    n_runs = len(initial_lengths)

    fidelities = np.empty(n_runs, dtype=np.float64)
    incorrects = np.empty(n_runs, dtype=np.int64)
    final_lengths = np.empty(n_runs, dtype=np.int64)

    for i, k in enumerate(initial_lengths):
        alice_basis = generate_bits(k)
        bob_basis = generate_bits(k)

        bob_key, kept = results(alice_basis, bob_basis, probs_arr, errs_arr)
        alice_key = alice_basis[kept]

        correctness, incorrect, length = check_keys(alice_key, bob_key)
        fidelities[i] = correctness
        incorrects[i] = incorrect
        final_lengths[i] = length

    save_data(fidelities, initial_lengths, incorrects, final_lengths, args.regime, b92=True, norm=args.norm)

    elapsed = time.perf_counter() - start
    print(f"b92_sim ({args.regime} regime) completed in {elapsed:.3f} s for {n_runs} runs.")


if __name__ == "__main__":
    main()
