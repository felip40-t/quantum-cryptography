"""
Script containing utility functions for the QKD simulations.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from qkd.constants import B92_STATE_ORDER, N, RUNS

def generate_bits(n: int):
    """
    Generate a random bit string as an int8 numpy array of length n.
    """
    return np.random.randint(0, 2, size=n, dtype=np.int8)

def check_keys(key1: np.ndarray, key2: np.ndarray):
    """
    Function to check the correctness of Bob's key compared to Alice's key.
    Returns the percentage of bits that match, the number of incorrect bits,
    and the total length of the keys.
    """
    key1 = np.asarray(key1)
    key2 = np.asarray(key2)
    counter = int(np.sum(key1 == key2))
    correctness = (counter / len(key1)) * 100
    incorrect = len(key1) - counter
    return correctness, incorrect, len(key1)

def save_data(fidelities: np.ndarray, initial_lengths: np.ndarray, incorrects: np.ndarray, final_len: np.ndarray, regime: str, b92: bool, norm: bool):
    """
    Function to save the data from the simulations in a csv file.
    """
    if b92:
        protocol = 'b92'
    else:
        protocol = 'bb84'
    df = pd.DataFrame({'Initial Key Length': initial_lengths, 'Correctness': fidelities, 'Incorrect Bits': incorrects, 'Final Key Length': final_len})
    if norm:
        regime += '_norm'
    output_path = (
        Path(__file__).parent.parent.parent / 'data' / f'{protocol}_data' /
        f'{N}_bits_{RUNS}_runs_{regime}.csv'
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

def renormalise_probabilities(prob_dict: dict):
    """
    Function to renormalise the probabilities in the given dictionary so that
    each (tx_basis, rx_basis) pair sums to 1 across the two bit values.
    For example '0AA' and '1AA' are combined so their probabilities sum to 1,
    giving P(Bob measures 0) and P(Bob measures 1) for Alice sending in basis A
    and Bob measuring in basis A.
    """
    renorm_dict = {}
    for state, (p0, e0) in prob_dict.items():
        anti_state = ('1' if state[0] == '0' else '0') + state[1:]
        p1, e1 = prob_dict[anti_state]
        total_p = p0 + p1
        new_p = p0 / total_p
        new_e = np.sqrt((p1 * e0)**2 + (p0 * e1)**2) / (total_p**2)
        renorm_dict[state] = (new_p, new_e)

    return renorm_dict

def pack_probabilities(prob_dict: dict, norm: bool = False):
    """
    Pack the 4-state B92 probability dict into two float arrays indexed by
    case = 2*alice_basis + bob_basis.
    """
    if norm:
        prob_dict = renormalise_probabilities(prob_dict)
    probs = np.array([prob_dict[k][0] for k in B92_STATE_ORDER], dtype=np.float64)
    errs = np.array([prob_dict[k][1] for k in B92_STATE_ORDER], dtype=np.float64)
    return probs, errs