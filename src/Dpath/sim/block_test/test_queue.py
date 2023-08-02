import pytest
from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim

from sim.queue import queue

class TestHarness( Component ):
    def construct( s, queue_instance ):
        s.src = stream.SourceRTL(Bits32)
        s.sink = stream.SinkRTL(Bits32)
        s.queue = queue_instance

        s.src.send //= s.queue.recv_msg
        s.queue.send_msg //= s.sink.recv

    def done(s):
        return s.src.done() and s.sink.done()

    def line_trace(s):
        return s.src.line_trace() + " > " + s.queue.line_trace() + " > " + s.sink.line_trace()

def function_source_msg():
    return [0x12345678, 0x87654321]

def function_sink_msg():
    return [0x12345678, 0x87654321]

test_case_table = mk_test_case_table([
    ( "msgs_source msgs_sink src_delay sink_delay"),
    [ "test_case_1", function_source_msg, function_sink_msg, 0, 0 ],
])

@pytest.mark.parametrize( **test_case_table )
def test( request, test_params, cmdline_opts ):
    queue_instance = queue(WIDTH=32) # set width to 32 bits
    th = TestHarness(queue_instance)

    msgs_source = test_params.msgs_source()
    msgs_source = [mk_bits(32)(m) for m in msgs_source]

    msgs_sink = test_params.msgs_sink()
    msgs_sink = [mk_bits(32)(m) for m in msgs_sink]

    print("Expecting", msgs_source, msgs_sink)

    th.set_param("top.src.construct",
        msgs=msgs_source,
        initial_delay=test_params.src_delay+3,
        interval_delay=test_params.src_delay )

    th.set_param("top.sink.construct",
        msgs=msgs_sink,
        initial_delay=test_params.sink_delay+3,
        interval_delay=test_params.sink_delay )

    cmdline_opts["dump_vcd"] = f'Queue_{request.node.name}'

    run_sim( th, cmdline_opts, duts=['queue'] )
