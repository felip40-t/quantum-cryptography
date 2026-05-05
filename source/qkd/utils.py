"""
Script containing utility functions for the QKD simulations.
"""

import numpy as np
from qkd.constants import B92_STATE_ORDER

def generate_bits(n):
    """
    Generate a random bit string as an int8 numpy array of length n.
    """
    return np.random.randint(0, 2, size=n, dtype=np.int8)

def check_keys(key1, key2):
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


def renormalise_probabilities(prob_dict):
    """
    Function to renormalise the probabilities in the given dictionary so that
    they sum to 1 for each key.
    For example combine '0AA' and '1AA' to get the probabilities for the case where
    Alice sends in basis A and Bob measures in basis A, regardless of the bit sent.
    """
    renorm_dict = {}
    for state in B92_STATE_ORDER:
        anti_state = ('1' if state[0] == '0' else '0') + state[1:]
        p0, e0 = prob_dict[state]
        p1, e1 = prob_dict[anti_state]
        total_p = p0 + p1
        new_p = p0 / total_p
        new_e = np.sqrt((p1 * e0)**2 + (p0 * e1)**2) / (total_p**2)
        renorm_dict[state] = (new_p, new_e)

    return renorm_dict

def pack_probabilities(prob_dict):
    """
    Pack the 4-state B92 probability dict into two float arrays indexed by
    case = 2*alice_basis + bob_basis.
    """
    prob_dict = renormalise_probabilities(prob_dict)
    probs = np.array([prob_dict[k][0] for k in B92_STATE_ORDER], dtype=np.float64)
    errs = np.array([prob_dict[k][1] for k in B92_STATE_ORDER], dtype=np.float64)
    return probs, errs