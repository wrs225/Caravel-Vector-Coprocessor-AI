#===============================================================================
# Floating Point Add/Subtract Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.fp_addsub import fp_addsub

def test_addition(cmdline_opts):
    addsub = fp_addsub(WIDTH=32)
    test_cases = [
        # Input1, Input2, Operation Type, Expected Result
        ('a b subtract y*'),
        [1.5, 2.5, 0, 4.0],
        [0.0, 0.0, 0, 0.0],
        [-3.2, 1.7, 0, -1.5],
        [100.123, -50.321, 0, 49.802],
        [10.0, 0.0, 0, 10.0],
    ]
    run_test_vector_sim(addsub, test_cases, cmdline_opts)

def test_subtraction(cmdline_opts):
    addsub = fp_addsub(WIDTH=32)
    test_cases = [
        # Input1, Input2, Operation Type, Expected Result
        ('a b subtract y*'),
        [5.0, 2.0, 1, 3.0],
        [0.0, 0.0, 1, 0.0],
        [-3.2, -1.7, 1, -1.5],
        [100.123, 50.321, 1, 49.802],
        [10.0, 10.0, 1, 0.0],
    ]
    run_test_vector_sim(addsub, test_cases, cmdline_opts)
