// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef _VMULTIPLIERWRAPPER__SYMS_H_
#define _VMULTIPLIERWRAPPER__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODULE CLASSES
#include "VMultiplierWrapper.h"

// SYMS CLASS
class VMultiplierWrapper__Syms : public VerilatedSyms {
  public:
    
    // LOCAL STATE
    const char* __Vm_namep;
    bool __Vm_didInit;
    
    // SUBCELL STATE
    VMultiplierWrapper*            TOPp;
    
    // CREATORS
    VMultiplierWrapper__Syms(VMultiplierWrapper* topp, const char* namep);
    ~VMultiplierWrapper__Syms() {}
    
    // METHODS
    inline const char* name() { return __Vm_namep; }
    
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

#endif  // guard
