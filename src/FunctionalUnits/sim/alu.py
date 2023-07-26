from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the ALU Verilog model

class ALU(VerilogPlaceholder, Component):

    def construct(self, WIDTH=32):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'ALUWrapper')

        self.A = InPort(mk_bits(WIDTH))
        self.B = InPort(mk_bits(WIDTH))
        self.C = InPort(mk_bits(WIDTH))
        self.AddSub = InPort(1)
        self.muxControl = InPort(1)
        self.outputControl = InPort(mk_bits(3))
        self.bitwiseControl = InPort(mk_bits(2))
        self.compControl = InPort(mk_bits(2))
        self.finalResult = OutPort(mk_bits(WIDTH))
        self.predicate = OutPort(1)
        