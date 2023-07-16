// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VFPAddSubWrapper.h for the primary calling header

#include "VFPAddSubWrapper.h"
#include "VFPAddSubWrapper__Syms.h"

//==========

VL_CTOR_IMP(VFPAddSubWrapper) {
    VFPAddSubWrapper__Syms* __restrict vlSymsp = __VlSymsp = new VFPAddSubWrapper__Syms(this, name());
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void VFPAddSubWrapper::__Vconfigure(VFPAddSubWrapper__Syms* vlSymsp, bool first) {
    if (0 && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
}

VFPAddSubWrapper::~VFPAddSubWrapper() {
    delete __VlSymsp; __VlSymsp=NULL;
}

void VFPAddSubWrapper::eval() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VFPAddSubWrapper::eval\n"); );
    VFPAddSubWrapper__Syms* __restrict vlSymsp = this->__VlSymsp;  // Setup global symbol table
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
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
            VL_FATAL_MT("fp_addsub.v", 54, "",
                "Verilated model didn't converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

void VFPAddSubWrapper::_eval_initial_loop(VFPAddSubWrapper__Syms* __restrict vlSymsp) {
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
            VL_FATAL_MT("fp_addsub.v", 54, "",
                "Verilated model didn't DC converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

VL_INLINE_OPT void VFPAddSubWrapper::_combo__TOP__1(VFPAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::_combo__TOP__1\n"); );
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->FPAddSubWrapper__DOT__v__DOT__a_mant_align 
        = ((0x1fU >= (0xffU & ((vlTOPp->a >> 0x17U) 
                               - (vlTOPp->b >> 0x17U))))
            ? ((0x7fffffU & vlTOPp->a) << (0xffU & 
                                           ((vlTOPp->a 
                                             >> 0x17U) 
                                            - (vlTOPp->b 
                                               >> 0x17U))))
            : 0U);
    vlTOPp->FPAddSubWrapper__DOT__v__DOT__sum = ((IData)(vlTOPp->subtract)
                                                  ? 
                                                 (vlTOPp->FPAddSubWrapper__DOT__v__DOT__a_mant_align 
                                                  - 
                                                  (0x7fffffU 
                                                   & vlTOPp->b))
                                                  : 
                                                 (vlTOPp->FPAddSubWrapper__DOT__v__DOT__a_mant_align 
                                                  + 
                                                  (0x7fffffU 
                                                   & vlTOPp->b)));
    vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_mant = 
        (0x7fffffU & vlTOPp->FPAddSubWrapper__DOT__v__DOT__sum);
    vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_exp_temp 
        = (0xffU & ((IData)(0xaU) + ((vlTOPp->a >> 0x17U) 
                                     + (VL_CLOG2_I(
                                                   (0x3ffU 
                                                    & (vlTOPp->FPAddSubWrapper__DOT__v__DOT__sum 
                                                       >> 0x16U))) 
                                        - (IData)(0x20U)))));
    vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_mant = 
        (((0xffU == (IData)(vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_exp_temp)) 
          | (0U == (IData)(vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_exp_temp)))
          ? 0U : (0x7fffffU & vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_mant));
    vlTOPp->y = ((((0xffU == (0xffU & (vlTOPp->a >> 0x17U))) 
                   & (0U != (0x7fffffU & vlTOPp->a))) 
                  | ((0xffU == (0xffU & (vlTOPp->b 
                                         >> 0x17U))) 
                     & (0U != (0x7fffffU & vlTOPp->b))))
                  ? 0xff800001U : (((((0xffU == (0xffU 
                                                 & (vlTOPp->a 
                                                    >> 0x17U))) 
                                      & (0U == (0x7fffffU 
                                                & vlTOPp->a))) 
                                     & ((1U & (vlTOPp->a 
                                               >> 0x1fU)) 
                                        != (IData)(vlTOPp->subtract))) 
                                    | (((0xffU == (0xffU 
                                                   & (vlTOPp->b 
                                                      >> 0x17U))) 
                                        & (0U == (0x7fffffU 
                                                  & vlTOPp->b))) 
                                       & ((1U & (vlTOPp->b 
                                                 >> 0x1fU)) 
                                          == (IData)(vlTOPp->subtract))))
                                    ? 0x7f800000U : 
                                   ((0x40000000U & 
                                     ((0x40000000U 
                                       & (vlTOPp->a 
                                          >> 1U)) ^ 
                                      ((IData)(vlTOPp->subtract) 
                                       << 0x1eU))) 
                                    | (((IData)(vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_exp_temp) 
                                        << 0x16U) | 
                                       (0x3fffffU & vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_mant)))));
}

void VFPAddSubWrapper::_eval(VFPAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::_eval\n"); );
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

void VFPAddSubWrapper::_eval_initial(VFPAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::_eval_initial\n"); );
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VFPAddSubWrapper::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::final\n"); );
    // Variables
    VFPAddSubWrapper__Syms* __restrict vlSymsp = this->__VlSymsp;
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VFPAddSubWrapper::_eval_settle(VFPAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::_eval_settle\n"); );
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

VL_INLINE_OPT QData VFPAddSubWrapper::_change_request(VFPAddSubWrapper__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::_change_request\n"); );
    VFPAddSubWrapper* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    // Change detection
    QData __req = false;  // Logically a bool
    __req |= ((vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_mant ^ vlTOPp->__Vchglast__TOP__FPAddSubWrapper__DOT__v__DOT__y_mant));
    VL_DEBUG_IF( if(__req && ((vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_mant ^ vlTOPp->__Vchglast__TOP__FPAddSubWrapper__DOT__v__DOT__y_mant))) VL_DBG_MSGF("        CHANGE: fp_addsub.v:32: FPAddSubWrapper.v.y_mant\n"); );
    // Final
    vlTOPp->__Vchglast__TOP__FPAddSubWrapper__DOT__v__DOT__y_mant 
        = vlTOPp->FPAddSubWrapper__DOT__v__DOT__y_mant;
    return __req;
}

#ifdef VL_DEBUG
void VFPAddSubWrapper::_eval_debug_assertions() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::_eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((reset & 0xfeU))) {
        Verilated::overWidthError("reset");}
    if (VL_UNLIKELY((clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((subtract & 0xfeU))) {
        Verilated::overWidthError("subtract");}
}
#endif  // VL_DEBUG

void VFPAddSubWrapper::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VFPAddSubWrapper::_ctor_var_reset\n"); );
    // Body
    reset = VL_RAND_RESET_I(1);
    clk = VL_RAND_RESET_I(1);
    a = VL_RAND_RESET_I(32);
    b = VL_RAND_RESET_I(32);
    subtract = VL_RAND_RESET_I(1);
    y = VL_RAND_RESET_I(32);
    FPAddSubWrapper__DOT__v__DOT__a_mant_align = VL_RAND_RESET_I(32);
    FPAddSubWrapper__DOT__v__DOT__sum = VL_RAND_RESET_I(32);
    FPAddSubWrapper__DOT__v__DOT__y_exp_temp = VL_RAND_RESET_I(8);
    FPAddSubWrapper__DOT__v__DOT__y_mant = VL_RAND_RESET_I(23);
    __Vchglast__TOP__FPAddSubWrapper__DOT__v__DOT__y_mant = VL_RAND_RESET_I(23);
}
