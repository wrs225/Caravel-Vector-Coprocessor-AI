from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the Floating Point Add/Sub Verilog model

class fp_addsub(VerilogPlaceholder, Component):

    def construct(self, WIDTH=32):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'FPAddSubWrapper')

        self.a = InPort(mk_bits(WIDTH))
        self.b = InPort(mk_bits(WIDTH))
        self.subtract = InPort(1)
        self.y = OutPort(mk_bits(WIDTH))