from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the Multiplier Verilog model

class Predicate_Register_File(VerilogPlaceholder, Component):

    def construct(self, ADDR_WIDTH=5, DATA_WIDTH=1, NUM_REGISTERS=32):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'predicate_register_file')

        self.read_addr1 = InPort(mk_bits(ADDR_WIDTH))
        self.read_addr2 = InPort(mk_bits(ADDR_WIDTH))

        self.write_addr1 = InPort(mk_bits(ADDR_WIDTH))
        self.write_addr2 = InPort(mk_bits(ADDR_WIDTH))
        self.write_enable = InPort(mk_bits(1))

        self.data_out = OutPort(mk_bits(DATA_WIDTH))
        self.data_in = InPort(mk_bits(DATA_WIDTH))        
