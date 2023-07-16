// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef _VADDSUBWRAPPER__SYMS_H_
#define _VADDSUBWRAPPER__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODULE CLASSES
#include "VAddSubWrapper.h"

// SYMS CLASS
class VAddSubWrapper__Syms : public VerilatedSyms {
  public:
    
    // LOCAL STATE
    const char* __Vm_namep;
    bool __Vm_didInit;
    
    // SUBCELL STATE
    VAddSubWrapper*                TOPp;
    
    // CREATORS
    VAddSubWrapper__Syms(VAddSubWrapper* topp, const char* namep);
    ~VAddSubWrapper__Syms() {}
    
    // METHODS
    inline const char* name() { return __Vm_namep; }
    
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

#endif  // guard
