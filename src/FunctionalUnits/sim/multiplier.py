from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the Multiplier Verilog model

class Multiplier(VerilogPlaceholder, Component):

    def construct(self, WIDTH=32):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'MultiplierWrapper')

        self.A = InPort(mk_bits(WIDTH))
        self.B = InPort(mk_bits(WIDTH))
        self.Result = OutPort(mk_bits(WIDTH))