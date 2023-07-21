#===============================================================================
# Float Multiplier Test
#===============================================================================

import random
from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim, config_model_with_cmdline_opts
from sim.fp_multiplier import fp_multiplier
from sim.block_test.utils import float_to_hex, ieee_754_to_float

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
        [float_to_hex(float('nan')), float_to_hex(float('-inf')), float_to_hex(float('-nan'))],
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

def test_overflow_to_infinity(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [float_to_hex(float('1.8e308')), float_to_hex(float('1.0')), float_to_hex(float('1.8e308'))],
        [float_to_hex(float('1.8e308')), float_to_hex(float('2.0')), float_to_hex(float('inf'))],
        [float_to_hex(float('-1.8e308')), float_to_hex(float('2.0')), float_to_hex(float('-inf'))],
    ], cmdline_opts)

def test_random(cmdline_opts):
    multiplier = fp_multiplier()
    multiplier = config_model_with_cmdline_opts(multiplier, cmdline_opts, duts=[])
    multiplier.apply(DefaultPassGroup())

    def tr(dut, a, b):
        # Write input value to input port
        dut.a @= a
        dut.b @= b
        
        retval = dut.y
        dut.sim_tick()
        return retval

    for _ in range(1000):
        a = random.uniform(-1e38, 1e38)
        b = random.uniform(-1e38, 1e38)
        actual_result = tr(multiplier, float_to_hex(a), float_to_hex(b))

        bit_expected = float_to_hex(a * b)
        clipped_expected = ieee_754_to_float(bit_expected)

        # Account for inf and nan, then check floats within tolerance
        assert (bit_expected == int(actual_result)) or \
            abs(clipped_expected - ieee_754_to_float(actual_result)) < 1e-7
