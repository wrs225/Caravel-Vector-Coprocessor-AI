#===============================================================================
# Float Add/Subtract Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.fp_addsub import fp_addsub
from sim.block_test.utils import float_to_hex
import random

def test_small(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(0.0), float_to_hex(0.0), 0x0, float_to_hex(0.0)],  # 0.0 + 0.0 = 0.0
        [float_to_hex(1.0), float_to_hex(2.0), 0x0, float_to_hex(3.0)],  # 1.0 + 2.0 = 3.0
        [float_to_hex(2.0), float_to_hex(1.0), 0x1, float_to_hex(1.0)],  # 2.0 - 1.0 = 1.0
        [float_to_hex(1.0), float_to_hex(2.0), 0x1, float_to_hex(-1.0)],  # 1.0 - 2.0 = -1.0
    ], cmdline_opts)

def test_large(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(1000.0), float_to_hex(1000.0), 0x0, float_to_hex(2000.0)],  # 1000.0 + 1000.0 = 2000.0
        [float_to_hex(1000.0), float_to_hex(100.0), 0x0, float_to_hex(1100.0)],  # 1000.0 + 100.0 = 1100.0
        [float_to_hex(1000.0), float_to_hex(100.0), 0x1, float_to_hex(900.0)],  # 1000.0 - 100.0 = 900.0
        [float_to_hex(100.0), float_to_hex(1000.0), 0x1, float_to_hex(-900.0)],  # 100.0 - 1000.0 = -900.0
    ], cmdline_opts)

def test_fractional(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(1.1), float_to_hex(2.2), 0x0, float_to_hex(3.3)],  # 1.1 + 2.2 = 3.3
        [float_to_hex(2.2), float_to_hex(1.1), 0x1, float_to_hex(1.1)],  # 2.2 - 1.1 = 1.1
        [float_to_hex(5.67), float_to_hex(3.21), 0x0, float_to_hex(8.88)],  # 5.67 + 3.21 = 8.88
        [float_to_hex(5.67), float_to_hex(3.21), 0x1, float_to_hex(2.46)],  # 5.67 - 3.21 = 2.46
        [float_to_hex(0.1), float_to_hex(0.2), 0x0, float_to_hex(0.3)],  # 0.1 + 0.2 = 0.3
        [float_to_hex(0.2), float_to_hex(0.1), 0x1, float_to_hex(0.1)],  # 0.2 - 0.1 = 0.1
    ], cmdline_opts)

def test_zero(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(0.0), float_to_hex(1.0), 0x0, float_to_hex(1.0)],  # 0.0 + 1.0 = 1.0
        [float_to_hex(1.0), float_to_hex(0.0), 0x0, float_to_hex(1.0)],  # 1.0 + 0.0 = 1.0
        [float_to_hex(1.0), float_to_hex(0.0), 0x1, float_to_hex(1.0)],  # 1.0 - 0.0 = 1.0
        [float_to_hex(0.0), float_to_hex(1.0), 0x1, float_to_hex(-1.0)],  # 0.0 - 1.0 = -1.0
    ], cmdline_opts)

def test_negative(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(-1.0), float_to_hex(-1.0), 0x0, float_to_hex(-2.0)],  # -1.0 + -1.0 = -2.0
        [float_to_hex(-1.0), float_to_hex(1.0), 0x0, float_to_hex(0.0)],  # -1.0 + 1.0 = 0.0
        [float_to_hex(1.0), float_to_hex(-1.0), 0x1, float_to_hex(2.0)],  # 1.0 - -1.0 = 2.0
        [float_to_hex(-1.0), float_to_hex(-1.0), 0x1, float_to_hex(0.0)],  # -1.0 - -1.0 = 0.0
    ], cmdline_opts)

def test_infinity(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(float('inf')), float_to_hex(1.0), 0x0, float_to_hex(float('inf'))],  # inf + 1.0 = inf
        [float_to_hex(float('-inf')), float_to_hex(1.0), 0x1, float_to_hex(float('-inf'))],  # -inf - 1.0 = -inf
        [float_to_hex(1.0), float_to_hex(float('inf')), 0x1, float_to_hex(float('-inf'))],  # 1.0 - inf = -inf
        [float_to_hex(float('inf')), float_to_hex(float('inf')), 0x1, float_to_hex(float('nan'))],  # inf - inf = nan
    ], cmdline_opts)

def test_nan(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(float('nan')), float_to_hex(1.0), 0x0, float_to_hex(float('nan'))],  # nan + 1.0 = nan
        [float_to_hex(float('nan')), float_to_hex(1.0), 0x1, float_to_hex(float('nan'))],  # nan - 1.0 = nan
        [float_to_hex(1.0), float_to_hex(float('nan')), 0x0, float_to_hex(float('nan'))],  # 1.0 + nan = nan
        [float_to_hex(1.0), float_to_hex(float('nan')), 0x1, float_to_hex(float('nan'))],  # 1.0 - nan = nan
    ], cmdline_opts)

def test_random(cmdline_opts):
    adder = fp_addsub()
    tests = []

    # generate 1000 random test cases
    for _ in range(1000):
        a = random.uniform(-1e10, 1e10)  # random float between -1e10 and 1e10
        b = random.uniform(-1e10, 1e10)  # random float between -1e10 and 1e10
        subtract = random.choice([0x0, 0x1])  # random choice between add or subtract
        expected_result = a - b if subtract else a + b

        tests.append([float_to_hex(a), float_to_hex(b), subtract, float_to_hex(expected_result)])

    run_test_vector_sim(adder, [('a       b       subtract y*')] + tests, cmdline_opts)
