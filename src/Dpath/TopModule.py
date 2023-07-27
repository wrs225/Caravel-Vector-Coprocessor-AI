from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.passes.backends.verilog import *

class TopModule( VerilogPlaceholder, Component ):

  # Constructor

  def construct( s ):

    # If translated into Verilog, we use the explicit name

    s.set_metadata( VerilogTranslationPass.explicit_module_name, 'top_module' )

    # Interface

    # Receive interface for load_queue
    s.load_recv = stream.ifcs.RecvIfcRTL( Bits64 )

    # Receive interface for instruction_queue
    s.instruction_recv = stream.ifcs.RecvIfcRTL( Bits32 )

    # Send interface for store_queue
    s.store_send = stream.ifcs.SendIfcRTL( Bits32 )

# Instantiate the Verilog module
topmodule = TopModule