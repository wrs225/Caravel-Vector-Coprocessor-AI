from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim, config_model_with_cmdline_opts
from .wishbone_interface_driver import wb_write, wb_read
from sim.WrapperBlock import WrapperBlock
from sim.block_test.utils import float_to_hex, ieee_754_to_float
import random

# Define some constants for the test
BASE_ADDRESS = 0x30000004
NUM_REGISTERS = 32
INSTRUCTION_ADDRESS = 0x30000000

# Define the opcodes for the instructions
VFADD_OPCODE = 0x07
VFMUL_OPCODE = 0x08
VFSUB_OPCODE = 0x10

# Tolerances for floating point comparisons
VFADD_VFSUB_TOLERANCE = 1e-4
VFMUL_TOLERANCE = 1e-4

def test_vfadd(cmdline_opts):
    # Instantiate and configure the DUT
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Run vfadd test logic
    vfadd_operation(dut)

def vfadd_operation(dut):
    inputs = [random.uniform(0, 100) for _ in range(NUM_REGISTERS * 2)]
    for i in range(NUM_REGISTERS * 2):
        register_address = BASE_ADDRESS + (i * 4)
        wb_write(dut, register_address, float_to_hex(inputs[i]))

    add_instruction = (VFADD_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

    for i in range(NUM_REGISTERS):
        register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)
        read_data_hex = wb_read(dut, register_address)
        read_data = ieee_754_to_float(read_data_hex)
        expected_result = inputs[i] + inputs[i + NUM_REGISTERS]
        assert abs(read_data - expected_result) <= VFADD_VFSUB_TOLERANCE, f"Error in VFADD. Input1: {inputs[i]}, Input2: {inputs[i + NUM_REGISTERS]}, Output: {read_data}, Expected: {expected_result} at address {register_address}"
    
    print("VFADD operation passed!")

def test_vfsub(cmdline_opts):
    # Instantiate and configure the DUT
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Run vfsub test logic
    vfsub_operation(dut)

def vfsub_operation(dut):
    inputs = [random.uniform(0, 100) for _ in range(NUM_REGISTERS * 2)]
    for i in range(NUM_REGISTERS * 2):
        register_address = BASE_ADDRESS + (i * 4)
        wb_write(dut, register_address, float_to_hex(inputs[i]))

    sub_instruction = (VFSUB_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, sub_instruction)

    for i in range(NUM_REGISTERS):
        register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)
        read_data_hex = wb_read(dut, register_address)
        read_data = ieee_754_to_float(read_data_hex)
        expected_result = inputs[i] - inputs[i + NUM_REGISTERS]
        assert abs(read_data - expected_result) <= VFADD_VFSUB_TOLERANCE, f"Error in VFSUB. Input1: {inputs[i]}, Input2: {inputs[i + NUM_REGISTERS]}, Output: {read_data}, Expected: {expected_result} at address {register_address}"

    print("VFSUB operation passed!")

def test_vfmul(cmdline_opts):
    # Instantiate and configure the DUT
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Run vfmul test logic
    vfmul_operation(dut)

def vfmul_operation(dut):
    inputs = [random.uniform(0, 100) for _ in range(NUM_REGISTERS * 2)]
    for i in range(NUM_REGISTERS * 2):
        register_address = BASE_ADDRESS + (i * 4)
        wb_write(dut, register_address, float_to_hex(inputs[i]))

    mul_instruction = (VFMUL_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, mul_instruction)

    for i in range(NUM_REGISTERS):
        register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)
        read_data_hex = wb_read(dut, register_address)
        read_data = ieee_754_to_float(read_data_hex)
        expected_result = inputs[i] * inputs[i + NUM_REGISTERS]
        assert abs(read_data - expected_result) <= VFMUL_TOLERANCE, f"Error in VFMUL. Input1: {inputs[i]}, Input2: {inputs[i + NUM_REGISTERS]}, Output: {read_data}, Expected: {expected_result} at address {register_address}"

    print("VFMUL operation passed!")
