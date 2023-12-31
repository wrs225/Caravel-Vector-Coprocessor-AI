#===============================================================================
# ALU Unit Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
#I changeed both of these lines from DPath.<package> to sim.<package> to make filestructure consistent
from sim.alu import ALU                                   
from sim.block_test.utils import float_to_hex

def test_add_sub_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b000, 0b00, 0b00, 0x7, '?'),
        (0x5, 0x2, 0x0, 0x1, 0x0, 0b000, 0b00, 0b00, 0x3, '?'),
        (0x5, 0x3, 0x0, 0x1, 0x1, 0b000, 0b00, 0b00, 0x5, '?'),  # Corrected expected result
    ], cmdline_opts)

def test_bitwise_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        # AND operation
        (0xF, 0x5, 0x0, 0x0, 0x0, 0b100, 0b00, 0b00, 0x5, '?'),
        (0xF, 0x2, 0x0, 0x0, 0x0, 0b100, 0b00, 0b00, 0x2, '?'),
        # OR operation
        (0xF, 0x5, 0x0, 0x0, 0x0, 0b100, 0b01, 0b00, 0xF, '?'),
        (0xF, 0x2, 0x0, 0x0, 0x0, 0b100, 0b01, 0b00, 0xF, '?'),
        # XOR operation
        (0xF, 0x5, 0x0, 0x0, 0x0, 0b100, 0b10, 0b00, 0xA, '?'),
        (0xF, 0x2, 0x0, 0x0, 0x0, 0b100, 0b10, 0b00, 0xD, '?'),
    ], cmdline_opts)

def test_mult_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (0x5, 0x3, 0x0, 0x0, 0x0, 0b010, 0b00, 0b00, 0xF, '?'),
        (0x2, 0x3, 0x0, 0x0, 0x0, 0b010, 0b00, 0b00, 0x6, '?'),
    ], cmdline_opts)

def test_comparison_unit(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        # VPSETZ operation
        (0x0, 0x0, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0000, '?', 1),
        (0x5, 0x0, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0000, '?', 0),
        # VPSETN operation
        (0x5, 0x0, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0001, '?', 1),
        (0x0, 0x0, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0001, '?', 0),
        # VPSET operation
        (0x5, 0x0, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0010, '?', 1),
        # VPSGE operation
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0011, '?', 1),
        # VPSLT operation
        (0x2, 0x5, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0100, '?', 1),
        # VPUGE operation
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0101, '?', 1),
        # VPULT operation
        (0x2, 0x5, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0110, '?', 1),
        # VPEQ operation
        (0x5, 0x5, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0111, '?', 1),
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b111, 0b00, 0b0111, '?', 0),
        # VPNEQ operation
        (0x5, 0x2, 0x0, 0x0, 0x0, 0b111, 0b00, 0b1000, '?', 1),
        (0x5, 0x5, 0x0, 0x0, 0x0, 0b111, 0b00, 0b1000, '?', 0),
    ], cmdline_opts)

def test_fp_addsub_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (float_to_hex(1.23), float_to_hex(2.34), 0x0, 0x0, 0x0, 0b001, 0b00, 0b00, float_to_hex(3.57), '?'),
        (float_to_hex(4.56), float_to_hex(1.23), 0x0, 0x1, 0x0, 0b001, 0b00, 0b00, float_to_hex(3.33), '?'),
    ], cmdline_opts)

def test_fp_mult_operation(cmdline_opts):
    alu = ALU()
    run_test_vector_sim(alu, [
        ('A B C AddSub muxControl outputControl bitwiseControl compControl finalResult* predicate*'),
        (float_to_hex(1.5), float_to_hex(2.0), 0x0, 0x0, 0x0, 0b011, 0b00, 0b00, float_to_hex(3.0), '?'),
    ], cmdline_opts)
