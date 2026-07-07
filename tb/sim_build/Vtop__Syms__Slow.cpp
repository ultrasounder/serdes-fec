// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(252);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_TOP = new VerilatedScope{this, "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_prbs7 = new VerilatedScope{this, "prbs7", "prbs7", "prbs7", -9, VerilatedScope::SCOPE_MODULE};
    // Set up scope hierarchy
    __Vhier.add(0, __Vscopep_prbs7);
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_TOP->varInsert("clk", &(TOP.clk), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("en", &(TOP.en), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("out", &(TOP.out), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY, 0, 0);
    __Vscopep_TOP->varInsert("rst", &(TOP.rst), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_prbs7->varInsert("clk", &(TOP.prbs7__DOT__clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_prbs7->varInsert("en", &(TOP.prbs7__DOT__en), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_prbs7->varInsert("fb", &(TOP.prbs7__DOT__fb), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY, 0, 0);
    __Vscopep_prbs7->varInsert("lfsr", &(TOP.prbs7__DOT__lfsr), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,6,0);
    __Vscopep_prbs7->varInsert("out", &(TOP.prbs7__DOT__out), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY, 0, 0);
    __Vscopep_prbs7->varInsert("rst", &(TOP.prbs7__DOT__rst), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
}

Vtop__Syms::~Vtop__Syms() {
    // Tear down scope hierarchy
    __Vhier.remove(0, __Vscopep_prbs7);
    // Clear keys from hierarchy map after values have been removed
    __Vhier.clear();
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_TOP, __Vscopep_TOP = nullptr);
    VL_DO_CLEAR(delete __Vscopep_prbs7, __Vscopep_prbs7 = nullptr);
    // Tear down sub module instances
}
