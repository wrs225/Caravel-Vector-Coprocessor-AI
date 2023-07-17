#===============================================================================
# Float Add/Subtract Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.fp_addsub import fp_addsub

def test_small(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [0x00000000, 0x00000000, 0x0, 0x00000000], # 0.0 + 0.0 = 0.0
        [0x3f800000, 0x40000000, 0x0, 0x40400000], # 1.0 + 2.0 = 3.0
        [0x40000000, 0x3f800000, 0x1, 0x3f800000], # 2.0 - 1.0 = 1.0
        [0x3f800000, 0x40000000, 0x1, 0xbf800000], # 1.0 - 2.0 = -1.0
    ], cmdline_opts)

def test_large(cmdline_opts):
    adder = fp_addsub()

    run_test_vector_sim(adder, [
        ('a       b       subtract y'),
        [0x447a0000, 0x447a0000, 0x0, 0x44fa0000], # 1000.0 + 1000.0 = 2000.0
        [0x447a0000, 0x42c80000, 0x0, 0x4486cccd], # 1000.0 + 100.0 = 1100.0
        [0x447a0000, 0x42c80000, 0x1, 0x446d5555], # 1000.0 - 100.0 = 900.0
        [0x42c80000, 0x447a0000, 0x1, 0xc46d5555], # 100.0 - 1000.0 = -900.0
    ], cmdline_opts)
