#===============================================================================
# Float Multiplier Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.fp_multiplier import fp_multiplier

def test_small(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [0x00000000, 0x00000000, 0x00000000], # 0.0 * 0.0 = 0.0
        [0x3f800000, 0x40000000, 0x40000000], # 1.0 * 2.0 = 2.0
        [0x40000000, 0x3f800000, 0x40000000], # 2.0 * 1.0 = 2.0
        [0x3f800000, 0xbf800000, 0xbf800000], # 1.0 * -1.0 = -1.0
    ], cmdline_opts)

def test_large(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [0x447a0000, 0x447a0000, 0x48f5c000], # 1000.0 * 1000.0 = 1000000.0
        [0x447a0000, 0x42c80000, 0x461c4000], # 1000.0 * 100.0 = 100000.0
        [0x447a0000, 0x3f800000, 0x42fa0000], # 1000.0 * 1.0 = 1000.0
        [0x42c80000, 0xbf800000, 0xc2c80000], # 100.0 * -1.0 = -100.0
    ], cmdline_opts)

def test_infinity(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [0x7f800000, 0x00000000, 0xffc00000], # +Infinity * 0.0 = NaN
        [0x7f800000, 0x7f800000, 0x7f800000], # +Infinity * +Infinity = +Infinity
        [0xff800000, 0xff800000, 0x7f800000], # -Infinity * -Infinity = +Infinity
        [0x7f800000, 0xff800000, 0xff800000], # +Infinity * -Infinity = -Infinity
    ], cmdline_opts)

def test_nan(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [0xffc00000, 0x00000000, 0xffc00000], # NaN * 0.0 = NaN
        [0xffc00000, 0x7f800000, 0xffc00000], # NaN * +Infinity = NaN
        [0xffc00000, 0x3f800000, 0xffc00000], # NaN * 1.0 = NaN
        [0xffc00000, 0xff800000, 0xffc00000], # NaN * -Infinity = NaN
    ], cmdline_opts)

def test_extremes(cmdline_opts):
    multiplier = fp_multiplier()

    run_test_vector_sim(multiplier, [
        ('a       b       y*'),
        [0x7f7fffff, 0x7f7fffff, 0x7f800000], # MAX_FLOAT * MAX_FLOAT = +Infinity
        [0x007fffff, 0x007fffff, 0x00000000], # MIN_FLOAT * MIN_FLOAT = 0.0
        [0x7f7fffff, 0xff7fffff, 0xff800000], # MAX_FLOAT * -MAX_FLOAT = -Infinity
        [0x007fffff, 0x807fffff, 0x80000000], # MIN_FLOAT * -MIN_FLOAT = -0.0
    ], cmdline_opts)
