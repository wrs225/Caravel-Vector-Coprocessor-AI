from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim, config_model_with_cmdline_opts
from .wishbone_interface_driver import wb_write, wb_read
from sim.WrapperBlock import WrapperBlock
import random

# Define some constants for the test
BASE_ADDRESS = 0x30000004
NUM_REGISTERS = 32
INSTRUCTION_ADDRESS = 0x30000000

# Define the opcodes for the instructions
VADD_OPCODE = 0x02
VSUB_OPCODE = 0x03
VMUL_OPCODE = 0x04
VAND_OPCODE = 0x09
VOR_OPCODE = 0x0A
VXOR_OPCODE = 0x0B

def random_test_vector_add(dut):
  # Generate random inputs
  inputs = [random.randint(0, 100) for _ in range(NUM_REGISTERS * 2)]

  # Store the inputs in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, inputs[i])

  # Perform the vector add operation
  add_instruction = (VADD_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    expected_result = inputs[i] + inputs[i + NUM_REGISTERS]
    assert read_data == expected_result, f"Read data {read_data} does not match expected result {expected_result} at address {register_address}"

  print("Random test for vector add operation passed!")

def test_random_vector_add( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the random test for vector add operation
  random_test_vector_add(dut)

def test_wrapper_block( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the load-store operation
  load_store_operation(dut)

def test_all_registers_block( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Test all registers
  all_registers_operation(dut)

def test_vector_add( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the vector add operation
  vector_add_operation(dut)

def test_vector_sub( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the vector sub operation
  vector_sub_operation(dut)

def test_vector_mul( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the vector mul operation
  vector_mul_operation(dut)

def test_vector_and( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the vector and operation
  vector_and_operation(dut)

def test_vector_or( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the vector or operation
  vector_or_operation(dut)

def test_vector_xor( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the vector xor operation
  vector_xor_operation(dut)

def load_store_operation(dut):
  # Define some constants for the test
  TEST_ADDRESS = 0x30000004
  TEST_DATA = 0xDEADBEEF

  # Perform a write operation (store) to the TEST_ADDRESS
  wb_write(dut, TEST_ADDRESS, TEST_DATA)

  # Perform a read operation (load) from the TEST_ADDRESS
  read_data = wb_read(dut, TEST_ADDRESS)

  # Verify that the read data matches the written data
  assert read_data == TEST_DATA, f"Read data {read_data} does not match written data {TEST_DATA}"

  print("Load-store operation passed!")

def all_registers_operation(dut):
  # Define some constants for the test
  BASE_ADDRESS = 0x30000004
  NUM_REGISTERS = 32 * 32

  # Create a list to store the test data for each register
  test_data_list = [i for i in range(NUM_REGISTERS)]  # Or any other function of i

  # First, write to all registers
  for i in range(NUM_REGISTERS):
    # Calculate the address of the current register
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes

    # Perform a write operation (store) to the current register
    wb_write(dut, register_address, test_data_list[i])

  # Then, read from all registers and verify the data
  for i in range(NUM_REGISTERS):
    # Calculate the address of the current register
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes

    # Perform a read operation (load) from the current register
    read_data = wb_read(dut, register_address)

    # Verify that the read data matches the written data
    assert read_data == test_data_list[i], f"Read data {read_data} does not match written data {test_data_list[i]} at address {register_address}"

  print("All register operation passed!")

def vector_add_operation(dut):
  # Define some constants for the test
  BASE_ADDRESS = 0x30000004
  NUM_REGISTERS = 32
  INSTRUCTION_ADDRESS = 0x30000000
  VADD_OPCODE = 0x02

  # Store 1 in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, 1)

  # Add the two vectors together
  # The instruction is encoded as follows:
  # - Bits [31:27]: Opcode
  # - Bits [25:21]: Destination vector register (2)
  # - Bits [20:16]: Source vector register 1 (0)
  # - Bits [15:11]: Source vector register 2 (1)
  # - Bits [10:0]: Unused
  add_instruction = (VADD_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, add_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    assert read_data == 2, f"Read data {read_data} does not match expected result 2 at address {register_address}"

  print("Vector add operation passed!")

def vector_sub_operation(dut):
  # Define some constants for the test
  BASE_ADDRESS = 0x30000004
  NUM_REGISTERS = 32
  INSTRUCTION_ADDRESS = 0x30000000

  # Store 1 in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, 1)

  # Subtract the two vectors
  sub_instruction = (VSUB_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, sub_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    assert read_data == 0, f"Read data {read_data} does not match expected result 0 at address {register_address}"

  print("Vector sub operation passed!")

def vector_mul_operation(dut):
  # Define some constants for the test
  BASE_ADDRESS = 0x30000004
  NUM_REGISTERS = 32
  INSTRUCTION_ADDRESS = 0x30000000

  # Store 1 in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, 1)

  # Multiply the two vectors
  mul_instruction = (VMUL_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, mul_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    assert read_data == 1, f"Read data {read_data} does not match expected result 1 at address {register_address}"

  print("Vector mul operation passed!")

def vector_and_operation(dut):
  # Define some constants for the test
  BASE_ADDRESS = 0x30000004
  NUM_REGISTERS = 32
  INSTRUCTION_ADDRESS = 0x30000000

  # Store 1 in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, 1)

  # Perform bitwise AND operation on the two vectors
  and_instruction = (VAND_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, and_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    assert read_data == 1, f"Read data {read_data} does not match expected result 1 at address {register_address}"

  print("Vector AND operation passed!")

def vector_or_operation(dut):
  # Define some constants for the test
  BASE_ADDRESS = 0x30000004
  NUM_REGISTERS = 32
  INSTRUCTION_ADDRESS = 0x30000000

  # Store 1 in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, 1)

  # Perform bitwise OR operation on the two vectors
  or_instruction = (VOR_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, or_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    assert read_data == 1, f"Read data {read_data} does not match expected result 1 at address {register_address}"

  print("Vector OR operation passed!")

def vector_xor_operation(dut):
  # Define some constants for the test
  BASE_ADDRESS = 0x30000004
  NUM_REGISTERS = 32
  INSTRUCTION_ADDRESS = 0x30000000

  # Store 1 in the first 32 * 2 registers
  for i in range(NUM_REGISTERS * 2):
    register_address = BASE_ADDRESS + (i * 4)  # Assuming each register is 4 bytes
    wb_write(dut, register_address, 1)

  # Perform bitwise XOR operation on the two vectors
  xor_instruction = (VXOR_OPCODE << 27) | (2 << 21) | (0 << 16) | (1 << 11)
  wb_write(dut, INSTRUCTION_ADDRESS, xor_instruction)

  # Read and check the results from the third vector register
  for i in range(NUM_REGISTERS):
    register_address = BASE_ADDRESS + ((i + NUM_REGISTERS * 2) * 4)  # Assuming each register is 4 bytes
    read_data = wb_read(dut, register_address)
    assert read_data == 0, f"Read data {read_data} does not match expected result 0 at address {register_address}"

  print("Vector XOR operation passed!")
