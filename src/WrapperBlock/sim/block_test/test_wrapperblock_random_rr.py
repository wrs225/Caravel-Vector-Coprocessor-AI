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
VSUB_OPCODE = 0x03
VMUL_OPCODE = 0x04

def random_test_vector_sub(dut):
  # Generate random inputs
  inputs = [Bits(32, random.randint(-100, 100)) for _ in range(NUM_REGISTERS * 2)]

  # Store the inputs in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, inputs[i])

  # Perform the vector sub operation
  sub_instruction = (VSUB_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, sub_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    expected_result = Bits(32, inputs[i].int() - inputs[i + NUM_REGISTERS].int())
    assert read_data == expected_result, f"Read data {read_data} does not match expected result {expected_result} at address {register_address}"

  print("Random test for vector sub operation passed!")

def random_test_vector_mul(dut):
  # Generate random inputs
  inputs = [Bits(32, random.randint(-10, 10)) for _ in range(NUM_REGISTERS * 2)]  # Limit to 10 to avoid overflow

  # Store the inputs in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, inputs[i])

  # Perform the vector mul operation
  mul_instruction = (VMUL_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, mul_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    expected_result = Bits(32, inputs[i].int() * inputs[i + NUM_REGISTERS].int())
    assert read_data == expected_result, f"Read data {read_data} does not match expected result {expected_result} at address {register_address}"

  print("Random test for vector mul operation passed!")

def test_random_vector_sub( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the random test for vector sub operation
  random_test_vector_sub(dut)

def test_random_vector_mul( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the random test for vector mul operation
  random_test_vector_mul(dut)
