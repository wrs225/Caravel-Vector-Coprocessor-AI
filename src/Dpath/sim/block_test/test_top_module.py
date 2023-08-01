from sim.TopModule import TopModule
from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
import pytest
import random

random.seed(0xdeadbeef)

def make_signed(value, bits):
    if value & (1 << (bits - 1)):
        return value - (1 << bits)
    else:
        return value

def generate_load_msg(addr, data):
    return (data << 32) | addr

def generate_instruction_msg(opcode, dest_reg, src_reg1, src_reg2):
    return (opcode << 27) | (dest_reg << 22) | (src_reg1 << 17) | (src_reg2 << 12)

def test_case_function_load_msg():
    # Generate some test data
    addr = 0x10
    load_data = 0x12345678

    # Generate the load message
    load_msg = generate_load_msg(addr, load_data)

    # Return the load message
    return [load_msg]

def test_case_function_instruction_msg():
    # Generate some test data
    opcode = 0x00
    dest_reg = 0x01
    src_reg1 = 0x02
    src_reg2 = 0x03

    # Generate the instruction message
    instruction_msg = generate_instruction_msg(opcode, dest_reg, src_reg1, src_reg2)

    # Return the instruction message
    return [instruction_msg]

def test_case_function_sink_msg():
    # Generate some test data
    addr = 0x10
    store_data = 0x12345678

    # Generate the sink message
    sink_msg = generate_load_msg(addr, store_data)

    # Return the sink message
    return [sink_msg]

test_case_table = mk_test_case_table([
  (                                   "msgs_load msgs_instruction msgs_sink      src_delay sink_delay"),
  [ "test_case_1",                     test_case_function_load_msg, test_case_function_instruction_msg, test_case_function_sink_msg, 0, 0 ],
])

class TestHarness( Component ):

  def construct( s, vector_accelerator, src_delay=0, sink_delay=0 ):

    # Instantiate models
    s.vector_accelerator = vector_accelerator

    s.src_load  = stream.SourceRTL( Bits64 )
    s.src_instruction = stream.SourceRTL( Bits32 )
    s.sink = stream.SinkRTL( Bits32 )  # Changed to Bits32

    # Connect
    s.src_load.send //= s.vector_accelerator.load_recv
    s.src_instruction.send //= s.vector_accelerator.instruction_recv
    s.vector_accelerator.store_send //= s.sink.recv

  def done( s ):
    return s.src_load.done() and s.src_instruction.done() and s.sink.done()

  def line_trace( s ):
    return s.src_load.line_trace() + " > " + s.src_instruction.line_trace() + " > " + s.vector_accelerator.line_trace() + " > " + s.sink.line_trace()

@pytest.mark.parametrize( **test_case_table )
def test( request, test_params, cmdline_opts ):

  # Instantiate the TopModule
  vector_accelerator = TopModule()

  # Pass the TopModule instance to the TestHarness
  th = TestHarness( vector_accelerator )

  msgs_load = test_params.msgs_load()
  msgs_load = [make_signed(m, 64) for m in msgs_load]

  msgs_instruction = test_params.msgs_instruction()
  msgs_instruction = [make_signed(m, 32) for m in msgs_instruction]

  msgs_sink = test_params.msgs_sink()
  msgs_sink = [make_signed(m, 32) for m in msgs_sink]  # Changed to 32

  print("Expecting", msgs_load, msgs_instruction, msgs_sink)

  th.set_param("top.src_load.construct",
    msgs=msgs_load,
    initial_delay=test_params.src_delay+3,
    interval_delay=test_params.src_delay )

  th.set_param("top.src_instruction.construct",
    msgs=msgs_instruction,
    initial_delay=test_params.src_delay+3,
    interval_delay=test_params.src_delay )

  th.set_param("top.sink.construct",
    msgs=msgs_sink,
    initial_delay=test_params.sink_delay+3,
    interval_delay=test_params.sink_delay )

  cmdline_opts["dump_vcd"] = f'VectorAccelerator_{request.node.name}'

  run_sim( th, cmdline_opts, duts=['vector_accelerator'] )
