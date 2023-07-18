#===============================================================================
# Bitwise Logical Operation Module Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.bitwise_operation_unit import BitwiseOperationUnit

def test_and_operation(cmdline_opts):
    logic_module = BitwiseOperationUnit()
    run_test_vector_sim(logic_module, [
        ('operandA operandB control result*'),
        (0xffffffff, 0x0, 0x0, 0x0),
        (0xffffffff, 0xffffffff, 0x0, 0xffffffff),
        (0x5, 0x2, 0x0, 0x0),
        (0x7, 0x3, 0x0, 0x3)
    ], cmdline_opts)

def test_or_operation(cmdline_opts):
    logic_module = BitwiseOperationUnit()
    run_test_vector_sim(logic_module, [
        ('operandA operandB control result*'),
        (0xffffffff, 0x0, 0x1, 0xffffffff),
        (0x5, 0x2, 0x1, 0x7),
        (0x7, 0x3, 0x1, 0x7),
        (0x0, 0x0, 0x1, 0x0)
    ], cmdline_opts)

def test_xor_operation(cmdline_opts):
    logic_module = BitwiseOperationUnit()
    run_test_vector_sim(logic_module, [
        ('operandA operandB control result*'),
        (0xffffffff, 0xffffffff, 0x2, 0x0),
        (0x5, 0x2, 0x2, 0x7),
        (0x7, 0x3, 0x2, 0x4),
        (0x0, 0x0, 0x2, 0x0)
    ], cmdline_opts)

def test_edge_cases(cmdline_opts):
    logic_module = BitwiseOperationUnit()
    run_test_vector_sim(logic_module, [
        ('operandA operandB control result*'),
        (0x0, 0x0, 0x0, 0x0),
        (0x0, 0x0, 0x1, 0x0),
        (0x0, 0x0, 0x2, 0x0),
        (0xffffffff, 0x0, 0x0, 0x0),
        (0xffffffff, 0x0, 0x1, 0xffffffff),
        (0xffffffff, 0x0, 0x2, 0xffffffff),
        (0xffffffff, 0xffffffff, 0x0, 0xffffffff),
        (0xffffffff, 0xffffffff, 0x1, 0xffffffff),
        (0xffffffff, 0xffffffff, 0x2, 0x0)
    ], cmdline_opts)
