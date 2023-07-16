// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary design header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef _VFPADDSUBWRAPPER_H_
#define _VFPADDSUBWRAPPER_H_  // guard

#include "verilated.h"

//==========

class VFPAddSubWrapper__Syms;

//----------

VL_MODULE(VFPAddSubWrapper) {
  public:
    
    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(reset,0,0);
    VL_IN8(clk,0,0);
    VL_IN8(subtract,0,0);
    VL_IN(a,31,0);
    VL_IN(b,31,0);
    VL_OUT(y,31,0);
    
    // LOCAL SIGNALS
    // Internals; generally not touched by application code
    CData/*7:0*/ FPAddSubWrapper__DOT__v__DOT__y_exp_temp;
    IData/*31:0*/ FPAddSubWrapper__DOT__v__DOT__a_mant_align;
    IData/*31:0*/ FPAddSubWrapper__DOT__v__DOT__sum;
    IData/*22:0*/ FPAddSubWrapper__DOT__v__DOT__y_mant;
    
    // LOCAL VARIABLES
    // Internals; generally not touched by application code
    IData/*22:0*/ __Vchglast__TOP__FPAddSubWrapper__DOT__v__DOT__y_mant;
    
    // INTERNAL VARIABLES
    // Internals; generally not touched by application code
    VFPAddSubWrapper__Syms* __VlSymsp;  // Symbol table
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(VFPAddSubWrapper);  ///< Copying not allowed
  public:
    /// Construct the model; called by application code
    /// The special name  may be used to make a wrapper with a
    /// single model invisible with respect to DPI scope names.
    VFPAddSubWrapper(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    ~VFPAddSubWrapper();
    
    // API METHODS
    /// Evaluate the model.  Application must call when inputs change.
    void eval();
    /// Simulation complete, run final blocks.  Application must call on completion.
    void final();
    
    // INTERNAL METHODS
  private:
    static void _eval_initial_loop(VFPAddSubWrapper__Syms* __restrict vlSymsp);
  public:
    void __Vconfigure(VFPAddSubWrapper__Syms* symsp, bool first);
  private:
    static QData _change_request(VFPAddSubWrapper__Syms* __restrict vlSymsp);
  public:
    static void _combo__TOP__1(VFPAddSubWrapper__Syms* __restrict vlSymsp);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _eval(VFPAddSubWrapper__Syms* __restrict vlSymsp);
  private:
#ifdef VL_DEBUG
    void _eval_debug_assertions();
#endif  // VL_DEBUG
  public:
    static void _eval_initial(VFPAddSubWrapper__Syms* __restrict vlSymsp) VL_ATTR_COLD;
    static void _eval_settle(VFPAddSubWrapper__Syms* __restrict vlSymsp) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard
