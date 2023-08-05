from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim, config_model_with_cmdline_opts
from .wishbone_interface_driver import wb_write, wb_read
from sim.WrapperBlock import WrapperBlock #changed this to sim., just so much easier than waiting 30 seconds

def test_wrapper_block( cmdline_opts ):
  # Instantiate the DUT (Device Under Test)
  dut = WrapperBlock()
  dut = config_model_with_cmdline_opts( dut, cmdline_opts, duts=[] )
  dut.apply( DefaultPassGroup( linetrace=False ) )

  # Reset the simulation
  dut.sim_reset()

  # Perform the load-store operation
  load_store_operation(dut)

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

if __name__ == "__main__":
  import sys
  test_wrapper_block( sys.argv[1:] )
