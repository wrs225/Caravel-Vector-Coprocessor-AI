#===============================================================================
# Float Multiplier Test
#===============================================================================

import random
from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.fp_multiplier import fp_multiplier
from sim.block_test.utils import float_to_hex

def test_small(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [float_to_hex(0.0), float_to_hex(0.0), float_to_hex(0.0)],
        [float_to_hex(1.0), float_to_hex(2.0), float_to_hex(2.0)],
        [float_to_hex(2.0), float_to_hex(1.0), float_to_hex(2.0)],
        [float_to_hex(1.0), float_to_hex(-1.0), float_to_hex(-1.0)],
    ], cmdline_opts)

def test_large(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [float_to_hex(1000.0), float_to_hex(1000.0), float_to_hex(1000000.0)],
        [float_to_hex(1000.0), float_to_hex(100.0), float_to_hex(100000.0)],
        [float_to_hex(1000.0), float_to_hex(1.0), float_to_hex(1000.0)],
        [float_to_hex(100.0), float_to_hex(-1.0), float_to_hex(-100.0)],
    ], cmdline_opts)

def test_infinity(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [float_to_hex(float('inf')), float_to_hex(0.0), float_to_hex(float('nan'))],
        [float_to_hex(float('inf')), float_to_hex(float('inf')), float_to_hex(float('inf'))],
        [float_to_hex(float('-inf')), float_to_hex(float('-inf')), float_to_hex(float('inf'))],
        [float_to_hex(float('inf')), float_to_hex(float('-inf')), float_to_hex(float('-inf'))],
    ], cmdline_opts)

def test_nan(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [float_to_hex(float('nan')), float_to_hex(0.0), float_to_hex(float('nan'))],
        [float_to_hex(float('nan')), float_to_hex(float('inf')), float_to_hex(float('nan'))],
        [float_to_hex(float('nan')), float_to_hex(1.0), float_to_hex(float('nan'))],
        [float_to_hex(float('nan')), float_to_hex(float('-inf')), float_to_hex(float('nan'))],
    ], cmdline_opts)

def test_extremes(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [float_to_hex(float('1.8e308')), float_to_hex(float('1.8e308')), float_to_hex(float('inf'))],
        [float_to_hex(float('1e-45')), float_to_hex(float('1e-45')), float_to_hex(0.0)],
        [float_to_hex(float('1.8e308')), float_to_hex(float('-1.8e308')), float_to_hex(float('-inf'))],
        [float_to_hex(float('1e-45')), float_to_hex(float('-1e-45')), float_to_hex(0.0)],
    ], cmdline_opts)

def test_random(cmdline_opts):
    multiplier = fp_multiplier()
    test_vectors = [('a', 'b', 'y*')]

    for _ in range(1000):
        a = random.uniform(-1e38, 1e38)
        b = random.uniform(-1e38, 1e38)
        expected_result = a * b
        test_vectors.append([float_to_hex(a), float_to_hex(b), float_to_hex(expected_result)])

    run_test_vector_sim(multiplier, test_vectors, cmdline_opts)
