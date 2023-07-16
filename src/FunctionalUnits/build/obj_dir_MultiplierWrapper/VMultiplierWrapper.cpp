// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VMultiplierWrapper.h for the primary calling header

#include "VMultiplierWrapper.h"
#include "VMultiplierWrapper__Syms.h"

//==========

VL_CTOR_IMP(VMultiplierWrapper) {
    VMultiplierWrapper__Syms* __restrict vlSymsp = __VlSymsp = new VMultiplierWrapper__Syms(this, name());
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void VMultiplierWrapper::__Vconfigure(VMultiplierWrapper__Syms* vlSymsp, bool first) {
    if (0 && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
}

VMultiplierWrapper::~VMultiplierWrapper() {
    delete __VlSymsp; __VlSymsp=NULL;
}

void VMultiplierWrapper::eval() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VMultiplierWrapper::eval\n"); );
    VMultiplierWrapper__Syms* __restrict vlSymsp = this->__VlSymsp;  // Setup global symbol table
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
#ifdef VL_DEBUG
    // Debug assertions
    _eval_debug_assertions();
#endif  // VL_DEBUG
    // Initialize
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) _eval_initial_loop(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Clock loop\n"););
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("Multiplier.v", 18, "",
                "Verilated model didn't converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

void VMultiplierWrapper::_eval_initial_loop(VMultiplierWrapper__Syms* __restrict vlSymsp) {
    vlSymsp->__Vm_didInit = true;
    _eval_initial(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        _eval_settle(vlSymsp);
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("Multiplier.v", 18, "",
                "Verilated model didn't DC converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

VL_INLINE_OPT void VMultiplierWrapper::_combo__TOP__1(VMultiplierWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::_combo__TOP__1\n"); );
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->Result = (vlTOPp->A * vlTOPp->B);
}

void VMultiplierWrapper::_eval(VMultiplierWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::_eval\n"); );
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

void VMultiplierWrapper::_eval_initial(VMultiplierWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::_eval_initial\n"); );
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VMultiplierWrapper::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::final\n"); );
    // Variables
    VMultiplierWrapper__Syms* __restrict vlSymsp = this->__VlSymsp;
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VMultiplierWrapper::_eval_settle(VMultiplierWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::_eval_settle\n"); );
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

VL_INLINE_OPT QData VMultiplierWrapper::_change_request(VMultiplierWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::_change_request\n"); );
    VMultiplierWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    // Change detection
    QData __req = false;  // Logically a bool
    return __req;
}

#ifdef VL_DEBUG
void VMultiplierWrapper::_eval_debug_assertions() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::_eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((reset & 0xfeU))) {
        Verilated::overWidthError("reset");}
    if (VL_UNLIKELY((clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
}
#endif  // VL_DEBUG

void VMultiplierWrapper::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VMultiplierWrapper::_ctor_var_reset\n"); );
    // Body
    reset = VL_RAND_RESET_I(1);
    clk = VL_RAND_RESET_I(1);
    A = VL_RAND_RESET_I(32);
    B = VL_RAND_RESET_I(32);
    Result = VL_RAND_RESET_I(32);
}
