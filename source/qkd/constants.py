"""
Constants for QKD implementation.
This contains the probabilities and uncertainties for both error regimes used in the simulations (high and low error).
Each regime is stored in a dictionary, where the keys are the 8 possible qubit and basis combinations, 
and the values are tuples containing the probability and uncertainty for that combination.
The following definitions are used for the keys and were 
'''
Definitions:
    We can send a 0 or a 1 in an A or B basis.
    A is the 0,90 basis
    B is the -45,45 basis

    In combination, we can send data as:
        0A - 0*
        1A - 90*
        0B - 45*
        1B - -45*
    using the above angles.

    They can be measured in A or B, giving 8 possible scenarios:
        0AA - Tx 0*, Rx 0*
        0AB - Tx 0*, Rx 45*
        0BA - Tx 45*, Rx 0*
        0BB - Tx 45*, Rx 45*
        1AA - Tx 90*, Rx 0*
        1AB - Tx 90*, Rx 45*
        1BA - Tx -45*, Rx 0*
        1BB - Tx -45*, Rx 45*
    each will have a corresponding probability that Bob measures a 0 (on-axis).

    For B92 protocol, Alice only sends states 0A = (0) and 0B = (1),
    but Bob still uses both bases to measure, so we have the following scenarios:
        0AA - Tx 0*, Rx 0*
        0AB - Tx 0*, Rx 45*
        0BA - Tx 45*, Rx 0*
        0BB - Tx 45*, Rx 45*.
    

'''
"""

RUNS = 100 # number of times to repeat the Monte Carlo simulation.
N = 2048 # number of bits in Alice's starting key

PROBABILITIES_LOW = {
    '0AA': (0.984194058, 0.0019738),
    '0AB': (0.460664777, 0.00120231),
    '0BA': (0.52466991, 0.0012733),
    '0BB': (0.981594554, 0.0019991),
    '1AA': (0.001551774, 0.0008767),
    '1AB': (0.511767302, 0.0012933),
    '1BA': (0.467991511, 0.0011976),
    '1BB': (0.000921125, 0.0008773)
}

PROBABILITIES_HIGH = {
    '0AA': (0.991714208, 0.045257911),
    '0AB': (0.550833094, 0.031513137),
    '0BA': (0.481797817, 0.029166418),
    '0BB': (0.986253124, 0.037687646),
    '1AA': (0.003161698, 0.022584011),
    '1AB': (0.437515014, 0.023950758),
    '1BA': (0.568813292, 0.029498697),
    '1BB': (0.006117577, 0.022383054)
}

# Order matches case = 2*alice_basis + bob_basis (0AA=0, 0AB=1, 0BA=2, 0BB=3).
B92_STATE_ORDER = ('0AA', '0AB', '0BA', '0BB')

