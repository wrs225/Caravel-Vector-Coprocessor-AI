#===============================================================================
# Comparison Unit Test
#===============================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sim.comparison_unit import comparison_unit

def test_vpsetz_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x0, 0x0, 0x0, 1),
        (0x5, 0x2, 0x0, 0)
    ], cmdline_opts)

def test_vpsetn_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x0, 0x0, 0x1, 0),
        (0x5, 0x2, 0x1, 1)
    ], cmdline_opts)

def test_vpset_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x0, 0x0, 0x2, 1),
    ], cmdline_opts)

def test_vpsge_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x5, 0x7, 0x3, 0),
        (0x7, 0x3, 0x3, 1),
        (0x0, 0x0, 0x3, 1)
    ], cmdline_opts)

def test_vpslt_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x5, 0x7, 0x4, 1),
        (0x7, 0x3, 0x4, 0),
        (0x0, 0x0, 0x4, 0)
    ], cmdline_opts)

def test_vpuge_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x5, 0x2, 0x5, 1),
        (0x2, 0x5, 0x5, 0)
    ], cmdline_opts)

def test_vpult_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x5, 0x7, 0x6, 1),
        (0x7, 0x3, 0x6, 0)
    ], cmdline_opts)

def test_vpeq_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x5, 0x5, 0x7, 1),
        (0x7, 0x3, 0x7, 0)
    ], cmdline_opts)

def test_vpneq_operation(cmdline_opts):
    comparison_module = comparison_unit()
    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        (0x5, 0x2, 0x8, 1),
        (0x7, 0x7, 0x8, 0)
    ], cmdline_opts)

def test_edge_cases(cmdline_opts):
    comparison_module = comparison_unit()
    
    max_unsigned = 0xFFFFFFFF
    max_signed = 0x7FFFFFFF
    min_signed = 0x80000000

    run_test_vector_sim(comparison_module, [
        ('in1 in2 control predicate*'),
        
        # VPSETZ
        (0x0, 0x0, 0x0, 1),
        (min_signed, 0x0, 0x0, 0),
        (max_signed, 0x0, 0x0, 0),

        # VPSETN
        (0x0, 0x0, 0x1, 0),
        (min_signed, 0x0, 0x1, 1),
        (max_signed, 0x0, 0x1, 1),

        # VPSGE
        (min_signed, max_signed, 0x3, 0),
        (max_signed, min_signed, 0x3, 1),
        (0x0, max_signed, 0x3, 0),
        (max_signed, 0x0, 0x3, 1),

        # VPSLT
        (min_signed, max_signed, 0x4, 1),
        (max_signed, min_signed, 0x4, 0),
        (0x0, max_signed, 0x4, 1),
        (max_signed, 0x0, 0x4, 0),

        # VPUGE
        (min_signed, max_signed, 0x5, 1), # 0x80000000 is larger than 0x7FFFFFFF when treated as unsigned
        (max_signed, min_signed, 0x5, 0), 
        (0x0, max_unsigned, 0x5, 0),
        (max_unsigned, 0x1, 0x5, 1),

        # VPULT
        (min_signed, max_unsigned, 0x6, 1), 
        (max_unsigned, 0x1, 0x6, 0),
        (0x0, max_unsigned, 0x6, 1),

        # VPEQ and VPNEQ
        (max_signed, max_signed, 0x7, 1),
        (min_signed, min_signed, 0x7, 1),
        (min_signed, max_signed, 0x8, 1),
        (max_signed, min_signed, 0x8, 1)

    ], cmdline_opts)
