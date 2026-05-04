"""
Script containing utility functions for the QKD simulations. 
"""

import numpy as np

def generate_bits(n):
    """
    Generate a bit string.
    """
    return [random.randint(0,1) for _ in range(n)]

def observations(qubits, bases):
    """
    Function to generate the observations of Bob based on the qubits sent by Alice
    and the bases used by Bob to measure. Returns a list of tuples containing
    the qubit sent and the basis used for each bit.
    """
    return list(zip(qubits, bases))

def check_keys(key1, key2):
    """
    Function to check the correctness of Bob's key compared to Alice's key. 
    Returns the percentage of bits that are correct, the number of incorrect bits,
    and the total length of the keys.
    """
    counter = 0
    for b in enumerate(key1):
        if b[1] == key2[b[0]]:
            counter += 1
    correctness = (counter/len(key1))*100
    return correctness, counter, len(key1)

def slice_probabilities(probs_dict):
    """
    Function to slice the probabilities and uncertainties from the probabilities
    dictionary to use in the B92 protocol. Returns a new dictionary with only 
    the relevant probabilities and uncertainties.
    """
    new_probs = {}
    for k in probs_dict:
        if k in ['0AA', '0AB', '0BA', '0BB']:
            new_probs[k] = probs_dict[k]
    return new_probs

def weighted_probabilities(probs1, uncerts1, probs2, uncerts2):
    """
    Function to calculate the weighted probabilities and uncertainties 
    from two sets of probabilities and uncertainties.
    Returns the new probabilities and uncertainties.
    """
    new_probs = []
    new_uncs = []
    for i in range(len(probs1)):
        val = np.array([probs1[i], probs2[i]])
        error = np.array([uncerts1[i], uncerts2[i]])
        wmtop = np.sum(val/(error**2))
        wmbot = np.sum(1/(error**2))
        weighted_mean = wmtop/wmbot
        error_in_wm = np.sqrt(1/(np.sum(1/(error**2))))
        new_probs.append(weighted_mean)
        new_uncs.append(error_in_wm)
    return new_probs,new_uncs

def alice_key(qubits,omit):
    """
    Function to generate Alice's key based on the qubits sent and the bits that were omitted.
    """
    final_key = []
    for a in omit:
        qubits[a] = 'omit'
    for j in enumerate(qubits):
        if j[1] == 0 or j[1] == 1:
            final_key.append(j[1])
    return final_key