"""
Simulate the BB84 protocol for different error regimes and save the data.
"""
import argparse
import time

import numpy as np

from qkd.constants import (
    PROBABILITIES_LOW, PROBABILITIES_HIGH, REPEATS, N
)
from qkd.utils import (
    generate_bits, check_keys, save_data,
)

def results(alice_bits, alice_basis, bob_basis, probs_dict):
    """
    Vectorised Monte Carlo step. For each bit, draws a per-observation
    probability sample around (prob, error) where the stored value is
    P(Bob measures 0) for that (bit, tx_basis, rx_basis) combination, then
    compares against a uniform draw to decide Bob's measurement outcome.
    """
    # Map (alice_bits, alice_basis, bob_basis) triples to case indices in the
    # order of PROBABILITIES_LOW/HIGH: 0AA, 0AB, 0BA, 0BB, 1AA, 1AB, 1BA, 1BB.
    case = 4 * alice_bits.astype(np.int64) + 2 * alice_basis.astype(np.int64) + bob_basis.astype(np.int64)
    probs_arr = np.array([v[0] for v in probs_dict.values()], dtype=np.float64)
    errs_arr = np.array([v[1] for v in probs_dict.values()], dtype=np.float64)
    # Generate sample probabilities for each bit based on case-specific mean and error.
    sampled_p = np.random.normal(probs_arr[case], errs_arr[case])
    # Clip probabilities to [0, 1] to ensure valid comparisons.
    np.clip(sampled_p, 0.0, 1.0, out=sampled_p)
    rand_vals = np.random.random(case.shape[0])

    # sampled_p is P(measure 0); rand_vals < sampled_p means Bob measured 0.
    measured_zero = rand_vals < sampled_p
    bob_key = np.where(measured_zero, 0, 1).astype(np.int8)
    return bob_key

def main():
    parser = argparse.ArgumentParser(description=
        'Simulate the BB84 protocol for different error regimes and save the data.'
    )
    parser.add_argument(
        "--regime",
        choices=["low", "high"],
        default="low",
        help="Error regime to use for probabilities and uncertainties (default: low).",
    )
    args = parser.parse_args()

    start = time.perf_counter()

    if args.regime == "high":
        probs_dict = PROBABILITIES_HIGH
    else:
        probs_dict = PROBABILITIES_LOW

    initial_lengths = np.tile(np.arange(32, N, 4), REPEATS)
    n_runs = len(initial_lengths)

    fidelities = np.empty(n_runs, dtype=np.float64)
    incorrects = np.empty(n_runs, dtype=np.int64)
    final_lengths = np.empty(n_runs, dtype=np.int64)

    for i, length in enumerate(initial_lengths):
        alice_bits = generate_bits(length)
        alice_basis = generate_bits(length)
        bob_basis = generate_bits(length)

        bob_key = results(alice_bits, alice_basis, bob_basis, probs_dict)

        # Check which basis choices match and filter keys accordingly
        matching_basis = alice_basis == bob_basis
        alice_key = alice_bits[matching_basis]
        bob_key = bob_key[matching_basis]
        correctness, incorrect, final_length = check_keys(alice_key, bob_key)
        fidelities[i] = correctness
        incorrects[i] = incorrect
        final_lengths[i] = final_length

    save_data(fidelities, initial_lengths, incorrects, final_lengths, args.regime, b92=False)

    elapsed = time.perf_counter() - start
    print(f"bb84_sim ({args.regime} regime) completed in {elapsed:.3f} s for {n_runs} runs.")
        

if __name__ == "__main__":
    main()
