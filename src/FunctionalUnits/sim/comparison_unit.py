from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the Comparison Unit Verilog model

class comparison_unit(VerilogPlaceholder, Component):

    def construct(self, WIDTH=32):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'ComparisonUnitWrapper')

        self.in1 = InPort(mk_bits(WIDTH))
        self.in2 = InPort(mk_bits(WIDTH))
        self.control = InPort(mk_bits(4))
        self.predicate = OutPort(mk_bits(1))
