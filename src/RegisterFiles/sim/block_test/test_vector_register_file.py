from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.vector_reg_file import VectorRegFile

def test_write_read(cmdline_opts):
    regfile = VectorRegFile(ADDR_WIDTH=5, DATA_WIDTH=32, NUM_REG=32, NUM_ELE=32)
    run_test_vector_sim(regfile, [
        ('reset rAddr1_1 rAddr2_1 rAddr1_2 rAddr2_2 wAddr1 wAddr2 wEnable wData rData1* rData2*'),
        (  0,     0x4,     0x2,     0x3,     0x1,    0x4,    0x2,     1,     0xF,     '?',    '?' ), # Write operation
        (  0,     0x4,     0x2,     0x3,     0x1,    0x3,    0x1,     0,     0x0,    0xF,    0x0 ), # Read operation
    ], cmdline_opts)

def test_reset(cmdline_opts):
    regfile = VectorRegFile(ADDR_WIDTH=5, DATA_WIDTH=32, NUM_REG=32, NUM_ELE=32)
    run_test_vector_sim(regfile, [
        ('reset rAddr1_1 rAddr2_1 rAddr1_2 rAddr2_2 wAddr1 wAddr2 wEnable wData rData1* rData2*'),
        (  1,     0x0,     0x0,     0x0,     0x0,    0x0,    0x0,     0,     0x0,     '?',    '?' ), # Reset all registers
        (  0,     0x4,     0x2,     0x3,     0x1,    0x3,    0x1,     0,     0x0,    0x0,    0x0 ), # Read should return 0 after reset
    ], cmdline_opts)

def test_varied_widths(cmdline_opts):
    regfile = VectorRegFile(ADDR_WIDTH=3, DATA_WIDTH=16, NUM_REG=8, NUM_ELE=8)
    run_test_vector_sim(regfile, [
        ('reset rAddr1_1 rAddr2_1 rAddr1_2 rAddr2_2 wAddr1 wAddr2 wEnable wData rData1* rData2*'),
        (  0,     0x2,     0x1,     0x3,     0x1,    0x2,    0x1,     1,    0xA,     '?',    '?' ), # Write operation
        (  0,     0x2,     0x1,     0x3,     0x1,    0x3,    0x1,     0,    0x0,    0xA,    0x0 ), # Read operation
    ], cmdline_opts)

def test_fill_register_file(cmdline_opts):
    regfile = VectorRegFile(ADDR_WIDTH=5, DATA_WIDTH=32, NUM_REG=32, NUM_ELE=32)
    test_vector = [('reset rAddr1_1 rAddr2_1 rAddr1_2 rAddr2_2 wAddr1 wAddr2 wEnable wData rData1* rData2*')]
    for i in range(32):
        for j in range(32):
            test_vector.append((0, i, j, i, j, i, j, 1, 0xFF, '?', '?')) # Fill entire register file with 0xFF
    for i in range(32):
        for j in range(32):
            test_vector.append((0, i, j, 0, 0, 0, 0, 0, 0, 0xFF, 0xFF)) # Read entire register file
    run_test_vector_sim(regfile, test_vector, cmdline_opts)

def test_overwrite_values(cmdline_opts):
    regfile = VectorRegFile(ADDR_WIDTH=5, DATA_WIDTH=32, NUM_REG=32, NUM_ELE=32)
    run_test_vector_sim(regfile, [
        ('reset rAddr1_1 rAddr2_1 rAddr1_2 rAddr2_2 wAddr1 wAddr2 wEnable wData rData1* rData2*'),
        (  0,     0x4,     0x2,     0x3,     0x1,    0x4,    0x2,     1,     0xFF,    '?',    '?' ), # Write operation
        (  0,     0x4,     0x2,     0x3,     0x1,    0x4,    0x2,     1,     0x0,    0xFF,   0x0 ), # Overwrite the same address with 0
        (  0,     0x4,     0x2,     0x3,     0x1,    0x3,    0x1,     0,     0x0,    0x0,    0x0 ), # Read should return 0
    ], cmdline_opts)
