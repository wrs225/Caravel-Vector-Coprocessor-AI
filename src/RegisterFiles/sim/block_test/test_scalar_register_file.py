from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.scalar_register_file import Scalar_Register_File # Assume Verilog import is named as this

def test_write_read(cmdline_opts):
    regfile = Scalar_Register_File(REG_DEPTH=32, REG_WIDTH=32, ADDR_WIDTH=5)
    run_test_vector_sim(regfile, [
        ('reset read_address write_address write_enable write_data read_data*'),
        (  0,      0x4,         0x4,          1,       0xFF,         '?' ), # Write operation
        (  0,      0x4,         0x3,          0,        0x0,        0xFF ), # Read operation
    ], cmdline_opts)

def test_reset(cmdline_opts):
    regfile = Scalar_Register_File(REG_DEPTH=32, REG_WIDTH=32, ADDR_WIDTH=5)
    run_test_vector_sim(regfile, [
        ('reset read_address write_address write_enable write_data read_data*'),
        (  1,      0x0,         0x0,          0,        0x0,         '?' ), # Reset all registers
        (  0,      0x4,         0x3,          0,        0x0,        0x00 ), # Read should return 0 after reset
    ], cmdline_opts)

def test_varied_widths(cmdline_opts):
    regfile = Scalar_Register_File(REG_DEPTH=8, REG_WIDTH=8, ADDR_WIDTH=3)
    run_test_vector_sim(regfile, [
        ('reset read_address write_address write_enable write_data read_data*'),
        (  0,      0x2,         0x2,          1,        0xF,         '?' ), # Write operation
        (  0,      0x2,         0x3,          0,        0x0,        0xF ), # Read operation
    ], cmdline_opts)

def test_fill_register_file(cmdline_opts):
    regfile = Scalar_Register_File(REG_DEPTH=32, REG_WIDTH=32, ADDR_WIDTH=5)
    test_vector = [('reset read_address write_address write_enable write_data read_data*')]
    for i in range(32):
        test_vector.append((0, i, i, 1, 0xFFFFFFFF, '?')) # Fill entire register file with 1s
    for i in range(32):
        test_vector.append((0, i, 0, 0, 0, 0xFFFFFFFF)) # Read entire register file
    run_test_vector_sim(regfile, test_vector, cmdline_opts)

def test_overwrite_values(cmdline_opts):
    regfile = Scalar_Register_File(REG_DEPTH=32, REG_WIDTH=32, ADDR_WIDTH=5)
    run_test_vector_sim(regfile, [
        ('reset read_address write_address write_enable write_data read_data*'),
        (  0,      0x4,         0x4,          1,        0x1,         '?' ), # Write operation
        (  0,      0x4,         0x4,          1,        0x0,         '?' ), # Overwrite the same address with 0
        (  0,      0x4,         0x3,          0,        0x0,        0x0 ), # Read operation, should return 0 after overwrite
    ], cmdline_opts)
