from pymtl3 import *
from pymtl3.passes.backends.verilog import *

# PyMTL wrapper for the BitwiseOperationUnit Verilog model

class BitwiseOperationUnit(VerilogPlaceholder, Component):

    def construct(self):
        self.set_metadata(VerilogTranslationPass.explicit_module_name, 'BitwiseOperationUnitWrapper')

        self.operandA = InPort(mk_bits(32))
        self.operandB = InPort(mk_bits(32))
        self.control = InPort(mk_bits(2))
        self.result = OutPort(mk_bits(32))
