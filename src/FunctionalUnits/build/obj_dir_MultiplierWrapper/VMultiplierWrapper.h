// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary design header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef _VMULTIPLIERWRAPPER_H_
#define _VMULTIPLIERWRAPPER_H_  // guard

#include "verilated.h"

//==========

class VMultiplierWrapper__Syms;

//----------

VL_MODULE(VMultiplierWrapper) {
  public:
    
    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(reset,0,0);
    VL_IN8(clk,0,0);
    VL_IN(A,31,0);
    VL_IN(B,31,0);
    VL_OUT(Result,31,0);
    
    // INTERNAL VARIABLES
    // Internals; generally not touched by application code
    VMultiplierWrapper__Syms* __VlSymsp;  // Symbol table
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(VMultiplierWrapper);  ///< Copying not allowed
  public:
    /// Construct the model; called by application code
    /// The special name  may be used to make a wrapper with a
    /// single model invisible with respect to DPI scope names.
    VMultiplierWrapper(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    ~VMultiplierWrapper();
    
    // API METHODS
    /// Evaluate the model.  Application must call when inputs change.
    void eval();
    /// Simulation complete, run final blocks.  Application must call on completion.
    void final();
    
    // INTERNAL METHODS
  private:
    static void _eval_initial_loop(VMultiplierWrapper__Syms* __restrict vlSymsp);
  public:
    void __Vconfigure(VMultiplierWrapper__Syms* symsp, bool first);
  private:
    static QData _change_request(VMultiplierWrapper__Syms* __restrict vlSymsp);
  public:
    static void _combo__TOP__1(VMultiplierWrapper__Syms* __restrict vlSymsp);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _eval(VMultiplierWrapper__Syms* __restrict vlSymsp);
  private:
#ifdef VL_DEBUG
    void _eval_debug_assertions();
#endif  // VL_DEBUG
  public:
    static void _eval_initial(VMultiplierWrapper__Syms* __restrict vlSymsp) VL_ATTR_COLD;
    static void _eval_settle(VMultiplierWrapper__Syms* __restrict vlSymsp) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard
