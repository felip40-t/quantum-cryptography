
"""
Created: Thu Oct 26 11:10:13 2023
Last Updated: Edited by Felipe Tcach 04/05/2026

@author: Charlie Fynn Perkins, UID: 10839865 0

This script has been adapted from the original code written by the author. It is now part of a forked repository
that aims to provide a clean and well-documented implementation of QKD protocols, specifically BB84 and B92.
The original code was developed as part of a laboratory project using optical components to simulate quantum key distribution.

"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from qkd.constants import PROBABILITIES_LOW, PROBABILITIES_HIGH


def main():
    parser = argparse.ArgumentParser(
        description="Plot single photon probabilities for all BB84 photon states."
    )
    parser.add_argument(
        "--regime",
        choices=["low", "high"],
        default="low",
        help="Error regime to use for probabilities and uncertainties (default: low).",
    )
    args = parser.parse_args()

    probs_dict = PROBABILITIES_LOW if args.regime == "low" else PROBABILITIES_HIGH

    # Each key (e.g. '1AA') encodes qubit, send-basis and measure-basis as defined in constants.py.
    system = tuple(probs_dict.keys())
    on_axis = np.array([probs_dict[k][0] for k in system]) * 100
    on_axis_err = np.array([probs_dict[k][1] for k in system]) * 100
    # Off-axis is the complementary outcome, so it shares the same propagated uncertainty.
    off_axis = 100 - on_axis
    off_axis_err = on_axis_err

    probability = {
        '0 (On Axis)': on_axis,
        '1 (Off Axis)': off_axis,
    }
    errors_by_attribute = {
        '0 (On Axis)': on_axis_err,
        '1 (Off Axis)': off_axis_err,
    }

    x = np.arange(len(system))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in probability.items():
        if attribute == "1 (Off Axis)":
            colour = "goldenrod"
        else:
            colour = "lightseagreen"
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width,
                       label=attribute, color=colour, zorder=2)
        ax.errorbar(x + offset, measurement,
                    yerr=errors_by_attribute[attribute], fmt=".", color="mediumvioletred", zorder=3)
        ax.bar_label(rects, padding=3, fontsize=7, fmt='%.1f', zorder=3)
        multiplier += 1

    ax.set_ylabel('Probability (%)')
    ax.set_title(
        f'Single Photon Probabilities for All Possible BB84 Photon States '
        f'({args.regime} error regime)'
    )

    major_ticks = np.arange(0, 120, 20)
    minor_ticks = np.arange(0, 120, 5)

    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)

    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2, zorder=0)
    ax.grid(which='major', alpha=0.5, zorder=0)

    ax.set_xticks(x + width / 2, system, rotation="vertical")
    ax.legend(loc=(0.1, 0.8))
    ax.set_ylim(0, 120)

    output_path = (
        Path(__file__).parent.parent / 'results' /
        f'photon_probabilities_{args.regime}.pdf'
    )
    plt.savefig(output_path, dpi=1000)


if __name__ == '__main__':
    main()
