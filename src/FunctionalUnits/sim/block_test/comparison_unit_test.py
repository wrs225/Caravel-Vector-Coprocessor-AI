#===============================================================================
# Comparison Unit Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.comparison_unit import comparison_unit

def test_equal_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0xffffffff, 0xffffffff, 0x0, 1),
        (0x5, 0x2, 0x0, 0),
        (0x7, 0x3, 0x0, 0),
        (0x0, 0x0, 0x0, 1)
    ], cmdline_opts)

def test_not_equal_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0xffffffff, 0x0, 0x1, 1),
        (0x5, 0x2, 0x1, 1),
        (0x7, 0x3, 0x1, 1),
        (0x0, 0x0, 0x1, 0)
    ], cmdline_opts)

def test_greater_than_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0xffffffff, 0x0, 0x2, 1),
        (0x5, 0x7, 0x2, 0),
        (0x7, 0x3, 0x2, 1),
        (0x0, 0x0, 0x2, 0)
    ], cmdline_opts)

def test_less_than_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0xffffffff, 0x0, 0x3, 0),
        (0x5, 0x7, 0x3, 1),
        (0x7, 0x3, 0x3, 0),
        (0x0, 0x0, 0x3, 0)
    ], cmdline_opts)

def test_edge_cases(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x0, 0x0, 0x0, 1),
        (0x0, 0x0, 0x1, 0),
        (0x0, 0x0, 0x2, 0),
        (0x0, 0x0, 0x3, 0),
        (0xffffffff, 0xffffffff, 0x0, 1),
        (0xffffffff, 0xffffffff, 0x1, 0),
        (0xffffffff, 0xffffffff, 0x2, 0),
        (0xffffffff, 0xffffffff, 0x3, 0)
    ], cmdline_opts)
