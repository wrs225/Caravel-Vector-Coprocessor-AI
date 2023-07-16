// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VAddSubWrapper.h for the primary calling header

#include "VAddSubWrapper.h"
#include "VAddSubWrapper__Syms.h"

//==========

VL_CTOR_IMP(VAddSubWrapper) {
    VAddSubWrapper__Syms* __restrict vlSymsp = __VlSymsp = new VAddSubWrapper__Syms(this, name());
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void VAddSubWrapper::__Vconfigure(VAddSubWrapper__Syms* vlSymsp, bool first) {
    if (0 && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
}

VAddSubWrapper::~VAddSubWrapper() {
    delete __VlSymsp; __VlSymsp=NULL;
}

void VAddSubWrapper::eval() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VAddSubWrapper::eval\n"); );
    VAddSubWrapper__Syms* __restrict vlSymsp = this->__VlSymsp;  // Setup global symbol table
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
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
            VL_FATAL_MT("AddSub.v", 23, "",
                "Verilated model didn't converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

void VAddSubWrapper::_eval_initial_loop(VAddSubWrapper__Syms* __restrict vlSymsp) {
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
            VL_FATAL_MT("AddSub.v", 23, "",
                "Verilated model didn't DC converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

VL_INLINE_OPT void VAddSubWrapper::_combo__TOP__1(VAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::_combo__TOP__1\n"); );
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->Result = ((IData)(vlTOPp->AddSub) ? (vlTOPp->A 
                                                 - vlTOPp->B)
                       : (vlTOPp->A + vlTOPp->B));
}

void VAddSubWrapper::_eval(VAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::_eval\n"); );
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

void VAddSubWrapper::_eval_initial(VAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::_eval_initial\n"); );
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VAddSubWrapper::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::final\n"); );
    // Variables
    VAddSubWrapper__Syms* __restrict vlSymsp = this->__VlSymsp;
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VAddSubWrapper::_eval_settle(VAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::_eval_settle\n"); );
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

VL_INLINE_OPT QData VAddSubWrapper::_change_request(VAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::_change_request\n"); );
    VAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    // Change detection
    QData __req = false;  // Logically a bool
    return __req;
}

#ifdef VL_DEBUG
void VAddSubWrapper::_eval_debug_assertions() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::_eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((reset & 0xfeU))) {
        Verilated::overWidthError("reset");}
    if (VL_UNLIKELY((clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((AddSub & 0xfeU))) {
        Verilated::overWidthError("AddSub");}
}
#endif  // VL_DEBUG

void VAddSubWrapper::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAddSubWrapper::_ctor_var_reset\n"); );
    // Body
    reset = VL_RAND_RESET_I(1);
    clk = VL_RAND_RESET_I(1);
    A = VL_RAND_RESET_I(32);
    AddSub = VL_RAND_RESET_I(1);
    B = VL_RAND_RESET_I(32);
    Result = VL_RAND_RESET_I(32);
}
