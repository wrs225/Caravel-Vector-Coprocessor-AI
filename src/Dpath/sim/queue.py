from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.passes.backends.verilog import *

class queue( VerilogPlaceholder, Component ):

  # Constructor
  def construct( s, WIDTH=8, DEPTH=16):

    # If translated into Verilog, we use the explicit name
    s.set_metadata( VerilogTranslationPass.explicit_module_name, 'queue_wrapper' )

    # Interface
    s.recv = stream.ifcs.RecvIfcRTL(mk_bits(WIDTH))
    
    s.send = stream.ifcs.SendIfcRTL(mk_bits(WIDTH))

# Instantiate the Verilog module
queue_instance = queue