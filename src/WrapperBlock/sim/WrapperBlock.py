from pymtl3 import *
from pymtl3.passes.backends.verilog import *

class WrapperBlock( VerilogPlaceholder, Component ):

  # Constructor
  def construct( s ):

    # Inputs
    s.wb_clk_i  = InPort ( Bits1 )
    s.wb_rst_i  = InPort ( Bits1 )
    s.wbs_stb_i = InPort ( Bits1 )
    s.wbs_cyc_i = InPort ( Bits1 )
    s.wbs_we_i  = InPort ( Bits1 )
    s.wbs_sel_i = InPort ( Bits4 )
    s.wbs_dat_i = InPort ( Bits32 )
    s.wbs_adr_i = InPort ( Bits32 )

    # Outputs
    s.wbs_ack_o = OutPort( Bits1 )
    s.wbs_dat_o = OutPort( Bits32 )

# Define the variable outside of the class
wrapperblock = WrapperBlock
