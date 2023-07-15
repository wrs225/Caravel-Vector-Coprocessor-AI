#===============================================================================
# Multiplier Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.multiplier import Multiplier

def test_positive_multiplication(cmdline_opts):
    multiplier = Multiplier(WIDTH=32)
    run_test_vector_sim(multiplier, [
        ('A B Result*'),
        (0x5, 0x2, 0xa),
        (0x7, 0x3, 0x15),
        (0xa, 0x0, 0x0),
        (0x1, 0xffffffff, 0xffffffff)
    ], cmdline_opts)

def test_zero_multiplication(cmdline_opts):
    multiplier = Multiplier(WIDTH=32)
    run_test_vector_sim(multiplier, [
        ('A B Result*'),
        (0x0, 0x2, 0x0),
        (0x0, 0x3, 0x0),
        (0x0, 0x0, 0x0)
    ], cmdline_opts)

def test_overflow(cmdline_opts):
    multiplier = Multiplier(WIDTH=32)
    run_test_vector_sim(multiplier, [
        ('A B Result*'),
        (0xffffffff, 0x2, 0xfffffffe),  # Maximum value multiplied by 2 (overflow ignored)
        (0x80000000, 0x2, 0x00000000),   # Maximum positive signed integer multiplied by 2 (overflow ignored)
        (0xffffffff, 0xffffffff, 0x1)    # Maximum value squared (overflow ignored)
    ], cmdline_opts)
