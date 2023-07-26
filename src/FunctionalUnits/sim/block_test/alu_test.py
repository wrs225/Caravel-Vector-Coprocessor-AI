#===============================================================================
# ALU Unit Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.alu import ALU
from sim.block_test.utils import float_to_hex

def test_add_sub_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b000, 0b00, 0b00, 0x7, 0),
        (0x5, 0x2, 0x0, 0x1, 0x0, 0b000, 0b00, 0b00, 0x3, 0),
    ], cmdline_opts)

def test_multiplier_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b010, 0b00, 0b00, 0xa, 0),
    ], cmdline_opts)

def test_bitwise_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b100, 0b00, 0b00, 0x0, 0),  # AND
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b100, 0b01, 0b00, 0x7, 0),  # OR
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b100, 0b10, 0b00, 0x7, 0),  # XOR
    ], cmdline_opts)

def test_comparison_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b000, 0b00, 0b01, 0x0, 0),  # EQUAL
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b000, 0b00, 0b10, 0x0, 1),  # NOT EQUAL
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b000, 0b00, 0b11, 0x0, 1),  # GREATER THAN
        (0x2, 0x5, 0x0, 0x0, 0x0, 0b000, 0b00, 0b00, 0x0, 1),  # LESS THAN
    ], cmdline_opts)

def test_fp_addsub_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (float_to_hex(1.23), float_to_hex(2.34), 0x0, 0x0, 0x0, 0b001, 0b00, 0b00, float_to_hex(3.57), 0),
        (float_to_hex(4.56), float_to_hex(1.23), 0x0, 0x1, 0x0, 0b001, 0b00, 0b00, float_to_hex(3.33), 0),
    ], cmdline_opts)

def test_fp_multiplier_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (float_to_hex(1.5), float_to_hex(2.0), 0x0, 0x0, 0x0, 0b011, 0b00, 0b00, float_to_hex(3.0), 0),
        (float_to_hex(3.5), float_to_hex(1.5), 0x0, 0x0, 0x0, 0b011, 0b00, 0b00, float_to_hex(5.25), 0),
    ], cmdline_opts)

def test_edge_cases(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (0x0, 0x0, 0x0, 0x0, 0x0, 0b000, 0b00, 0b00, 0x0, 0),
        (0xffffffff, 0xffffffff, 0x0, 0x1, 0x0, 0b000, 0b00, 0b00, 0x0, 0),
    ], cmdline_opts)
