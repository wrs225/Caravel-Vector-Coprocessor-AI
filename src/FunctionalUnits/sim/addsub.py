from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the AddSub Verilog model

class AddSub(VerilogPlaceholder, Component):

    def construct(self, WIDTH=32):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'AddSubWrapper')

        self.A = InPort(mk_bits(WIDTH))
        self.B = InPort(mk_bits(WIDTH))
        self.AddSub = InPort(1)
        self.Result = OutPort(mk_bits(WIDTH))