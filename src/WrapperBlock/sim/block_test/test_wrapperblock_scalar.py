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
    # Generate random inputs
    inputs = [random.randint(0, 100) for _ in range(NUM_REGISTERS)]
    scalar = random.randint(0, 100)

    # Store the inputs in the first 32 registers
    for i in range(NUM_REGISTERS):
        register_address = DATA_START_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
        wb_write(dut, register_address, inputs[i])

    # Store the scalar
    wb_write(dut, SCALAR_ADDRESS, scalar)

    # Perform the scalar add operation
    add_instruction = (VSADD_OPCODE << 27) | (1 << 21) | (0 << 16) | (0 << 11)
    wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

    # Read and check the results from the second vector register
    for i in range(NUM_REGISTERS):
        register_address = DATA_START_ADDRESS + ((i + NUM_REGISTERS) * 4)  # Assuming each register is 4 bytes
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
