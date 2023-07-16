#===============================================================================
# Add/Subtract Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.addsub import AddSub

def test_small(cmdline_opts):
    adder = AddSub(WIDTH=32)

    run_test_vector_sim(adder, [
        ('A B AddSub Result*'),
        [0x0, 0x0, 0x0, 0x0],
        [0x0, 0x0, 0x1, 0x0],
        [0x0, 0x1, 0x0, 0x1],
        [0x1, 0x0, 0x0, 0x1],
        [0x1, 0x0, 0x1, 0x1],
        [0xbeef, 0xc040ff, 0x0, 0xc0ffee],
        [0xc0ffee, 0xc040ff, 0x1, 0xbeef]
    ], cmdline_opts)

def test_add_large(cmdline_opts):
    adder = AddSub(WIDTH=32)

    run_test_vector_sim(adder, [
        ('A B AddSub Result*'),
        [0xf4240, 0x10c8e0, 0x0, 0x200b20],
        [0x200b20, 0xf4240, 0x0, 0x2f4d60],
        [0x77359400, 0x77359400, 0x0, 0xee6b2800],
        [0xee6b2800, 0xee6b2800, 0x0, 0xdcd65000]
    ], cmdline_opts)

def test_sub_large(cmdline_opts):
    adder = AddSub(WIDTH=32)

    run_test_vector_sim(adder, [
        ('A B AddSub Result*'),
        [0x0, 0x1, 0x1, 0xffffffff],
        [0xffffffff, 0xeeeeeeee, 0x1, 0x11111111],
        [0xeeeeeeee, 0xffffffff, 0x1, 0xeeeeeeef]
    ], cmdline_opts)