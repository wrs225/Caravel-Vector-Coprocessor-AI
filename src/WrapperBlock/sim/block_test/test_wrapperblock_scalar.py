from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim, config_model_with_cmdline_opts
from .wishbone_interface_driver import wb_write, wb_read
from sim.WrapperBlock import WrapperBlock
import random

# Define the new range of addresses
START_ADDRESS = 0x30001004
END_ADDRESS = 0x30001080
NUM_REGISTERS = (END_ADDRESS - START_ADDRESS) // 4 + 1  # Assuming each register is 4 bytes
INSTRUCTION_ADDRESS = 0x30000000

DATA_START_ADDRESS = 0x30000004
SCALAR_ADDRESS = 0x30001004

VSADD_OPCODE = 0x06
VPSET_OPCODE = 0x0E

def vpset_instruction(dut, Pdest, Ssrc):
    instruction = (VPSET_OPCODE << 27) | (Pdest << 21) | (Ssrc << 16)
    wb_write(dut, INSTRUCTION_ADDRESS, instruction)

def read_write_operation(dut):
    # Create a list to store the test data for each register
    test_data_list = [random.randint(0, 0xFFFFFFFF) for _ in range(NUM_REGISTERS)]  # Generate random 32-bit data for each register

    # Write to all registers in the new range
    for i in range(NUM_REGISTERS):
        register_address = START_ADDRESS + (i * 4)
        wb_write(dut, register_address, test_data_list[i])

    # Read from all registers in the new range and verify the data
    for i in range(NUM_REGISTERS):
        register_address = START_ADDRESS + (i * 4)
        read_data = wb_read(dut, register_address)
        assert read_data == test_data_list[i], f"Read data {read_data} does not match written data {test_data_list[i]} at address {register_address}"

    print("Read-write operation for the new address range passed!")

def scalar_add_operation(dut):
    # Define some constants for the test
    DATA_START_ADDRESS = 0x30000004
    NUM_REGISTERS = 32
    INSTRUCTION_ADDRESS = 0x30000000
    SCALAR_ADDRESS = 0x30001004
    VSADD_OPCODE = 0x06

    # Generate random inputs
    inputs = [random.randint(0, 100) for _ in range(NUM_REGISTERS)]
    scalar = random.randint(0, 100)

    # Store the inputs in the first 32 registers
    for i in range(NUM_REGISTERS):
        register_address = DATA_START_ADDRESS + (i * 4)
        wb_write(dut, register_address, inputs[i])

    # Store the scalar
    wb_write(dut, SCALAR_ADDRESS, scalar)

    # Set the proper register (replace with the correct values for Pdest and Ssrc)
    Pdest = 1
    Ssrc = 0
    vpset_instruction(dut, Pdest, Ssrc)

    # Perform the scalar add operation
    add_instruction = (VSADD_OPCODE << 27) | (Pdest << 21) | (Ssrc << 16) | (0 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

    # Read and check the results from the second vector register
    for i in range(NUM_REGISTERS):
        register_address = DATA_START_ADDRESS + ((i + NUM_REGISTERS) * 4)
        read_data = wb_read(dut, register_address)
        expected_result = inputs[i] + scalar
        assert read_data == expected_result, f"Read data {read_data} does not match expected result {expected_result} at address {register_address}"

    print("Scalar add operation passed!")



def test_new_address_range(cmdline_opts):
    # Instantiate the DUT (Device Under Test)
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Perform the read-write test for the new address range
    read_write_operation(dut)

def test_scalar_add(cmdline_opts):
    # Instantiate the DUT (Device Under Test)
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Perform the scalar add operation
    scalar_add_operation(dut)

def scalar_add_edge_cases(dut):
    # Define some constants for the test
    DATA_START_ADDRESS = 0x30000004
    SCALAR_ADDRESS = 0x30001004
    INSTRUCTION_ADDRESS = 0x30000000
    VSADD_OPCODE = 0x06
    NUM_REGISTERS = 32

    # Case 1: Overflow and underflow
    inputs = [0xFFFFFFFF, 0x7FFFFFFF, 0x80000000, 0x00000001] * (NUM_REGISTERS // 4)
    scalar = 0x00000001

    # Store the inputs
    for i, value in enumerate(inputs):
        register_address = DATA_START_ADDRESS + (i * 4)
        wb_write(dut, register_address, value)

    # Store the scalar
    wb_write(dut, SCALAR_ADDRESS, scalar)

    # Set the Pdest and Ssrc registers using the provided function
    Pdest = 1
    Ssrc = 0
    vpset_instruction(dut, Pdest, Ssrc)

    # Perform the scalar add operation
    add_instruction = (VSADD_OPCODE << 27) | (Pdest << 21) | (Ssrc << 16) | (0 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

    # Expected results considering a wrap-around for overflows
    expected_results = [0x00000000, 0x80000000, 0x80000001, 0x00000002] * (NUM_REGISTERS // 4)

    # Read and check the results
    for i, expected in enumerate(expected_results):
        register_address = DATA_START_ADDRESS + ((i + NUM_REGISTERS) * 4)
        read_data = wb_read(dut, register_address)
        assert read_data == expected, f"Read data {read_data} does not match expected result {expected} at address {register_address}"

    print("Scalar add edge cases passed!")


def test_scalar_add_edge_cases(cmdline_opts):
    # Instantiate the DUT (Device Under Test)
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Perform the scalar add edge cases
    scalar_add_edge_cases(dut)

def scalar_add_with_zeros(dut):
    # Define some constants for the test
    DATA_START_ADDRESS = 0x30000004
    SCALAR_ADDRESS = 0x30001004
    INSTRUCTION_ADDRESS = 0x30000000
    VSADD_OPCODE = 0x06
    NUM_REGISTERS = 32

    # Inputs are all zeros and scalar is zero
    inputs_zero = [0 for _ in range(NUM_REGISTERS)]
    scalar_zero = 0

    # Store the inputs
    for i, value in enumerate(inputs_zero):
        register_address = DATA_START_ADDRESS + (i * 4)
        wb_write(dut, register_address, value)

    # Store the scalar
    wb_write(dut, SCALAR_ADDRESS, scalar_zero)

    # Set the Pdest and Ssrc registers using the provided function
    Pdest = 1
    Ssrc = 0
    vpset_instruction(dut, Pdest, Ssrc)

    # Perform the scalar add operation
    add_instruction = (VSADD_OPCODE << 27) | (Pdest << 21) | (Ssrc << 16) | (0 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

    # Read and check the results
    for i in range(NUM_REGISTERS):
        register_address = DATA_START_ADDRESS + ((i + NUM_REGISTERS) * 4)
        read_data = wb_read(dut, register_address)
        assert read_data == 0, f"Read data {read_data} is not zero at address {register_address}"

    print("Scalar add with zeros test passed!")


def complementary_value_test(dut):
    # Define some constants for the test
    DATA_START_ADDRESS = 0x30000004
    SCALAR_ADDRESS = 0x30001004
    INSTRUCTION_ADDRESS = 0x30000000
    VSADD_OPCODE = 0x06
    NUM_REGISTERS = 32

    # Inputs negate the scalar
    scalar_complement = random.randint(1, 100)
    inputs_complement = [-scalar_complement for _ in range(NUM_REGISTERS)]

    # Store the inputs
    for i, value in enumerate(inputs_complement):
        register_address = DATA_START_ADDRESS + (i * 4)
        wb_write(dut, register_address, value)

    # Store the scalar
    wb_write(dut, SCALAR_ADDRESS, scalar_complement)

    # Set the Pdest and Ssrc registers using the provided function
    Pdest = 1
    Ssrc = 0
    vpset_instruction(dut, Pdest, Ssrc)

    # Perform the scalar add operation
    add_instruction = (VSADD_OPCODE << 27) | (Pdest << 21) | (Ssrc << 16) | (0 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

    # Read and check the results
    for i in range(NUM_REGISTERS):
        register_address = DATA_START_ADDRESS + ((i + NUM_REGISTERS) * 4)
        read_data = wb_read(dut, register_address)
        assert read_data == 0, f"Read data {read_data} is not zero at address {register_address}"

    print("Complementary value test passed!")


def test_scalar_add_with_zeros(cmdline_opts):
    # Instantiate the DUT (Device Under Test)
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Perform the scalar add with zeros test
    scalar_add_with_zeros(dut)

def test_complementary_value(cmdline_opts):
    # Instantiate the DUT (Device Under Test)
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Perform the complementary value test
    complementary_value_test(dut)

def boundary_address_test(dut):
    # Generate random values for the start and end of the address range
    start_value = random.randint(0, 0xFFFFFFFF)
    end_value = random.randint(0, 0xFFFFFFFF)

    # Write to the starting address
    wb_write(dut, START_ADDRESS, start_value)

    # Write to the ending address
    wb_write(dut, END_ADDRESS, end_value)

    # Read from the starting address and verify
    read_start_value = wb_read(dut, START_ADDRESS)
    assert read_start_value == start_value, f"Read data {read_start_value} does not match written data {start_value} at start address {START_ADDRESS}"

    # Read from the ending address and verify
    read_end_value = wb_read(dut, END_ADDRESS)
    assert read_end_value == end_value, f"Read data {read_end_value} does not match written data {end_value} at end address {END_ADDRESS}"

    print("Boundary address test passed!")

def test_boundary_address(cmdline_opts):
    # Instantiate the DUT (Device Under Test)
    dut = WrapperBlock()
    dut = config_model_with_cmdline_opts(dut, cmdline_opts, duts=[])
    dut.apply(DefaultPassGroup(linetrace=False))

    # Reset the simulation
    dut.sim_reset()

    # Perform the boundary address test
    boundary_address_test(dut)
