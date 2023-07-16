#===============================================================================
# Floating Point Add/Subtract Test
#===============================================================================

import struct
from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.fp_addsub import fp_addsub

def float_list_to_hex(float_list):
    """
    Converts a list of floating-point values to their hexadecimal representation (single-precision).
    """
    hex_list = [hex(struct.unpack('!I', struct.pack('!f', value))[0]) for value in float_list]
    return hex_list

def test_addition(cmdline_opts):
    addsub = fp_addsub(WIDTH=32)
    test_cases = [
        # Input1, Input2, Operation Type, Expected Result
        [1.5, 2.5, 0.0, 4.0],
        [0.0, 0.0, 0.0, 0.0],
        [-3.2, 1.7, 0.0, -1.5],
        [100.123, -50.321, 0, 49.802],
        [10.0, 0.0, 0, 10.0],
    ]
    test_cases = [float_list_to_hex(test) for test in test_cases]
    test_cases.insert(0, ('a b subtract y*'))
    run_test_vector_sim(addsub, test_cases, cmdline_opts)

def test_subtraction(cmdline_opts):
    addsub = fp_addsub(WIDTH=32)
    test_cases = [
        # Input1, Input2, Operation Type, Expected Result
        [5.0, 2.0, 1, 3.0],
        [0.0, 0.0, 1, 0.0],
        [-3.2, -1.7, 1, -1.5],
        [100.123, 50.321, 1, 49.802],
        [10.0, 10.0, 1, 0.0],
    ]
    test_cases = [float_list_to_hex(test) for test in test_cases]
    test_cases.insert(0, ('a b subtract y*'))
    run_test_vector_sim(addsub, test_cases, cmdline_opts)
