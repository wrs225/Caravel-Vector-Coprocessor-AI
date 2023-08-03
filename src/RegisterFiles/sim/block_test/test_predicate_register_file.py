from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.predicate_register_file import Predicate_Register_File

def test_write_read(cmdline_opts):
    regfile = Predicate_Register_File(ADDR_WIDTH=5, DATA_WIDTH=1, NUM_REGISTERS=32)
    run_test_vector_sim(regfile, [
        ('reset read_addr1 read_addr2 write_addr1 write_addr2 write_enable data_in data_out*'),
        (  0,     0x4,      0x2,        0x4,        0x2,         1,         1,        '?' ), # Write operation
        (  0,     0x4,      0x2,        0x3,        0x1,         0,         0,        0x1 ), # Read operation
    ], cmdline_opts)

def test_reset(cmdline_opts):
    regfile = Predicate_Register_File(ADDR_WIDTH=5, DATA_WIDTH=1, NUM_REGISTERS=32)
    run_test_vector_sim(regfile, [
        ('reset read_addr1 read_addr2 write_addr1 write_addr2 write_enable data_in data_out*'),
        (  1,     0x0,      0x0,        0x0,        0x0,         0,         0,        '?' ), # Reset all registers
        (  0,     0x4,      0x2,        0x3,        0x1,         0,         0,        0x0 ), # Read should return 0 after reset
    ], cmdline_opts)

def test_varied_widths(cmdline_opts):
    regfile = Predicate_Register_File(ADDR_WIDTH=3, DATA_WIDTH=2, NUM_REGISTERS=8)
    run_test_vector_sim(regfile, [
        ('reset read_addr1 read_addr2 write_addr1 write_addr2 write_enable data_in data_out*'),
        (  0,     0x2,      0x1,        0x2,        0x1,         1,        0x3,       '?' ), # Write operation
        (  0,     0x2,      0x1,        0x3,        0x1,         0,        0x0,       0x3 ), # Read operation
    ], cmdline_opts)

def test_fill_register_file(cmdline_opts):
    regfile = Predicate_Register_File(ADDR_WIDTH=5, DATA_WIDTH=1, NUM_REGISTERS=32)
    test_vector = [('reset read_addr1 read_addr2 write_addr1 write_addr2 write_enable data_in data_out*')]
    for i in range(32):
        for j in range(32):
            test_vector.append((0, i, j, i, j, 1, 1, '?')) # Fill entire register file with 1s
    for i in range(32):
        for j in range(32):
            test_vector.append((0, i, j, 0, 0, 0, 0, 1)) # Read entire register file
    run_test_vector_sim(regfile, test_vector, cmdline_opts)

def test_overwrite_values(cmdline_opts):
    regfile = Predicate_Register_File(ADDR_WIDTH=5, DATA_WIDTH=1, NUM_REGISTERS=32)
    run_test_vector_sim(regfile, [
        ('reset read_addr1 read_addr2 write_addr1 write_addr2 write_enable data_in data_out*'),
        (  0,     0x4,      0x2,        0x4,        0x2,         1,         1,        '?' ), # Write operation
        (  0,     0x4,      0x2,        0x4,        0x2,         1,         0,        0x1 ), # Overwrite the same address with 0
        (  0,     0x4,      0x2,        0x3,        0x1,         0,         0,        0x0 ), # Read operation, should return 0 after overwrite
    ], cmdline_opts)
