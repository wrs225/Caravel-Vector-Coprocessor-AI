from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim, config_model_with_cmdline_opts
from pymtl3.datatypes import Bits
from .wishbone_interface_driver import wb_write, wb_read
from sim.WrapperBlock import WrapperBlock
import random

# Define some constants for the test
BASE_ADDRESS = 0x30000004
NUM_REGISTERS = 32
INSTRUCTION_ADDRESS = 0x30000000

# Define the opcodes for the instructions
VAND_OPCODE = 0x09
VOR_OPCODE = 0x0A
VXOR_OPCODE = 0x0B

def random_test_vector_and(dut):
  # Generate random inputs
  inputs = [Bits(32, random.randint(-100, 100)) for _ in range(NUM_REGISTERS * 2)]

  # Store the inputs in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, inputs[i])

  # Perform the vector bitwise AND operation
  and_instruction = (VAND_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, and_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    expected_result = Bits(32, inputs[i].int() & inputs[i + NUM_REGISTERS].int())
    assert read_data == expected_result, f"Read data {read_data} does not match expected result {expected_result} at address {register_address}"

  print("Random test for vector bitwise AND operation passed!")

def random_test_vector_or(dut):
  # Generate random inputs
  inputs = [Bits(32, random.randint(-100, 100)) for _ in range(NUM_REGISTERS * 2)]

  # Store the inputs in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, inputs[i])

  # Perform the vector bitwise OR operation
  or_instruction = (VOR_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, or_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    expected_result = Bits(32, inputs[i].int() | inputs[i + NUM_REGISTERS].int())
    assert read_data == expected_result, f"Read data {read_data} does not match expected result {expected_result} at address {register_address}"

  print("Random test for vector bitwise OR operation passed!")

def random_test_vector_xor(dut):
  # Generate random inputs
  inputs = [Bits(32, random.randint(-100, 100)) for _ in range(NUM_REGISTERS * 2)]

  # Store the inputs in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, inputs[i])

  # Perform the vector bitwise XOR operation
  xor_instruction = (VXOR_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, xor_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    expected_result = Bits(32, inputs[i].int() ^ inputs[i + NUM_REGISTERS].int())
    assert read_data == expected_result, f"Read data {read_data} does not match expected result {expected_result} at address {register_address}"

  print("Random test for vector bitwise XOR operation passed!")

def test_random_vector_and( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the random test for vector bitwise AND operation
  random_test_vector_and(dut)

def test_random_vector_or( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the random test for vector bitwise OR operation
  random_test_vector_or(dut)

def test_random_vector_xor( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the random test for vector bitwise XOR operation
  random_test_vector_xor(dut)
