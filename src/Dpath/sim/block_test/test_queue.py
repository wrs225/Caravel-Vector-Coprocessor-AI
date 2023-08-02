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

        s.src.send //= s.queue.recv
        s.queue.send //= s.sink.recv

    def done(s):
        return s.src.done() and s.sink.done()

    def line_trace(s):
        return s.src.line_trace() + " > " + s.queue.line_trace() + " > " + s.sink.line_trace()

def function_source_msg_test_case_1():
    return [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10]

def function_source_msg_test_case_2():
    return [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8]

def function_source_msg_test_case_3():
    # 20 messages, more than the depth of the queue
    return list(range(1, 21))

def function_sink_msg_test_case_1():
    return [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10]

def function_sink_msg_test_case_2():
    return [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8]

def function_sink_msg_test_case_3():
    # Expecting all 20 messages from the source, since the queue should not drop any messages
    return list(range(1, 21))

def function_source_msg_test_case_4():
    return [0x1] * 50 # 50 messages

def function_source_msg_test_case_5():
    return [0x2, 0x4] * 25 # 50 messages

def function_sink_msg_test_case_4():
    return [0x1] * 50 # Expecting the same 50 messages

def function_sink_msg_test_case_5():
    return [0x2, 0x4] * 25 # Expecting the same 50 messages

test_case_table = mk_test_case_table([
    ( "msgs_source msgs_sink src_delay sink_delay"),
    [ "test_case_1", function_source_msg_test_case_1, function_sink_msg_test_case_1, 0, 0 ],
    [ "test_case_2", function_source_msg_test_case_2, function_sink_msg_test_case_2, 1, 2 ],
    [ "test_case_3", function_source_msg_test_case_3, function_sink_msg_test_case_3, 0, 0 ],
    [ "test_case_4", function_source_msg_test_case_4, function_sink_msg_test_case_4, 3, 1 ],
    [ "test_case_5", function_source_msg_test_case_5, function_sink_msg_test_case_5, 5, 5 ],
    [ "test_case_6", function_source_msg_test_case_1, function_sink_msg_test_case_1, 10, 0 ],
    [ "test_case_7", function_source_msg_test_case_2, function_sink_msg_test_case_2, 0, 10 ],
    [ "test_case_8", function_source_msg_test_case_3, function_sink_msg_test_case_3, 5, 5 ],
    [ "test_case_9", function_source_msg_test_case_4, function_sink_msg_test_case_4, 0, 5 ],
    [ "test_case_10", function_source_msg_test_case_5, function_sink_msg_test_case_5, 7, 3 ],
])

@pytest.mark.parametrize( **test_case_table )
def test( request, test_params, cmdline_opts ):
    queue_instance = queue(WIDTH=32, DEPTH=16) # set width to 32 bits and depth to 16
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
