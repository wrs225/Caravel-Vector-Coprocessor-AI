from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the Scalar Register File Verilog model

class Scalar_Register_File(VerilogPlaceholder, Component):

    def construct(self, REG_DEPTH=32, REG_WIDTH=32, ADDR_WIDTH=5):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'scalar_register_file')

        self.read_address = InPort(mk_bits(ADDR_WIDTH))
        self.write_address = InPort(mk_bits(ADDR_WIDTH))
        self.write_data = InPort(mk_bits(REG_WIDTH))
        self.write_enable = InPort(mk_bits(1))
        self.read_data = OutPort(mk_bits(REG_WIDTH))     
