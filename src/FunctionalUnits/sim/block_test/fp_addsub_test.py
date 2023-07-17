#===============================================================================
# Float Add/Subtract Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.fp_addsub import fp_addsub
from sim.block_test.utils import float_to_hex

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
    adder = fp_addsub(WIDTH=32)

    run_test_vector_sim(adder, [
        ('a       b       subtract y*'),
        [float_to_hex(1.1), float_to_hex(2.2), 0x0, float_to_hex(3.3)],  # 1.1 + 2.2 = 3.3
        [float_to_hex(2.2), float_to_hex(1.1), 0x1, float_to_hex(1.1)],  # 2.2 - 1.1 = 1.1
        [float_to_hex(5.67), float_to_hex(3.21), 0x0, float_to_hex(8.88)],  # 5.67 + 3.21 = 8.88
        [float_to_hex(5.67), float_to_hex(3.21), 0x1, float_to_hex(2.46)],  # 5.67 - 3.21 = 2.46
        [float_to_hex(0.1), float_to_hex(0.2), 0x0, float_to_hex(0.3)],  # 0.1 + 0.2 = 0.3
        [float_to_hex(0.2), float_to_hex(0.1), 0x1, float_to_hex(0.1)],  # 0.2 - 0.1 = 0.1
    ], cmdline_opts)
