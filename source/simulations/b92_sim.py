# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:33:30 2023

@author: felipe
BB92 code

"""


import numpy as np
import random
import argparse
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from qkd.constants import REPEATS, N, PROBABILITIES_LOW, PROBABILITIES_HIGH
from qkd.utils import (
    generate_bits, check_keys, observations, 
    slice_probabilities, alice_key
)


def results(observation, prob_dict):
    """
    Function to generate Bob's key based on the observations and the probabilities.
    """
    unfiltered_key = []
    clean_key = []
    omitted_bits = []

    for ob in observation:
        # Generate new probabilities based on the uncertainties for each observation.
        new_probs = {}
        for key, p in prob_dict.items():
            prob = p[0]
            error = p[1]
            new_p = random.normalvariate(prob, error)
            if new_p > 1:
                new_p = 1
            elif new_p < 0:
                new_p = 0
            new_probs[key] = new_p
        rando_num = random.uniform(0,1)

        # Case 0AA - Tx = 0', Rx = 0'
        if ob == (0,0):
            if rando_num < new_probs['0AA']:
                unfiltered_key.append('omit') # Measured 0'
            else:
                unfiltered_key.append(1) # Measured 90'
        # Case 0AB - Tx = 0', Rx = 45'
        elif ob == (0,1):
            if rando_num < new_probs['0AB']:
                unfiltered_key.append('omit') # Measured 45'
            else:
                unfiltered_key.append(0) # Measured -45'
        # Case 0BA - Tx = 45', Rx = 0'
        elif ob == (1,0):
            if rando_num < new_probs['0BA']:
                unfiltered_key.append('omit') # Measured 0'
            else:
                unfiltered_key.append(1) # Measured 90'
        # Case 0BB - Tx = 45', Rx = 45'
        elif ob == (1,1):
            if rando_num < new_probs['0BB']:
                unfiltered_key.append('omit') # Measured 45'
            else:
                unfiltered_key.append(0) # Measured -45'
    
    for j in enumerate(unfiltered_key):
        if j[1] == 0 or j[1] == 1:
            clean_key.append(j[1])
        else:
            omitted_bits.append(j[0])
    
    return clean_key, omitted_bits


def save_data(fidelities, bit_lengths, incorrects, final_len):
    """
    Function to save the data from the simulations in a csv file.
    """
    df = pd.DataFrame({'Initial Key Length': bit_lengths, 'Correctness': fidelities, 'Incorrect Bits': incorrects, 'Final Key Length': final_len})
    output_path = (
        Path(__file__).parent.parent / 'data' / 'b92_data' /
        f'{N}_bits_{REPEATS}_repeats.csv'
    )
    df.to_csv(output_path, index=False)


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
    args = parser.parse_args()

    if args.regime == "low":
        probs = slice_probabilities(PROBABILITIES_LOW)
    elif args.regime == "high":
        probs = slice_probabilities(PROBABILITIES_HIGH)

    percents = []
    bit_lengths = []
    incorrects = []
    final_length = []

    for i in range(REPEATS):
        for j in np.arange(32,N,4):
            bit_lengths.append(j)

    for k in bit_lengths:
        alice_qubits = generate_bits(k)
        bob_bases = generate_bits(k)

        obs = observations(alice_qubits, bob_bases)
        bob_key, omit = results(obs, probs, uncerts)
        alice_key = alice_key(alice_qubits, omit)

        percents.append(check_keys(alice_key, bob_key)[0])
        incorrects.append(check_keys(alice_key, bob_key)[1])
        final_length.append(check_keys(alice_key, bob_key)[2])
    
    save_data(percents, bit_lengths, incorrects, final_length)

if __name__ == "__main__":
    main()