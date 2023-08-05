from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the Multiplier Verilog model

class VectorRegFile(VerilogPlaceholder, Component):

    def construct(self, ADDR_WIDTH=5, DATA_WIDTH=32, NUM_REG=32, NUM_ELE=32):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'vector_register_file')

        self.rAddr1_1 = InPort(mk_bits(ADDR_WIDTH))
        self.rAddr2_1 = InPort(mk_bits(ADDR_WIDTH))
        self.rData1 = OutPort(mk_bits(DATA_WIDTH))

        self.rAddr1_2 = InPort(mk_bits(ADDR_WIDTH))
        self.rAddr2_2 = InPort(mk_bits(ADDR_WIDTH))
        self.rData2 = OutPort(mk_bits(DATA_WIDTH))

        self.wAddr1 = InPort(mk_bits(ADDR_WIDTH))
        self.wAddr2 = InPort(mk_bits(ADDR_WIDTH))
        self.wData = InPort(mk_bits(DATA_WIDTH))
        self.wEnable = InPort(mk_bits(1))    
