from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the Floating Point Add/Sub Verilog model

class fp_addsub(VerilogPlaceholder, Component):

    def construct(self):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'FPAddSubWrapper')

        self.a = InPort(mk_bits(32))
        self.b = InPort(mk_bits(32))
        self.subtract = InPort(1)
        self.y = OutPort(mk_bits(32))