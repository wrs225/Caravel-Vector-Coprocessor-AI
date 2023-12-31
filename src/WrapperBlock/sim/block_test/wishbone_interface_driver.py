from pymtl3 import *
from copy import deepcopy

def wb_tr( dut, stb, cyc, we, sel, dat, adr):
    dut.wb_rst_i  @= 0
    dut.wbs_stb_i @= stb
    dut.wbs_cyc_i @= cyc
    dut.wbs_we_i  @= we
    dut.wbs_sel_i @= sel
    dut.wbs_dat_i @= dat
    dut.wbs_adr_i @= adr

    # Save the values of dut.wbs_ack_o and dut.wbs_dat_o
    ack = deepcopy(dut.wbs_ack_o)
    dat = deepcopy(dut.wbs_dat_o)

    dut.sim_tick()

    return ack, dat

def wb_write(dut, address, data, timeout=1000):
    # Start the transaction
    ack, _ = wb_tr(dut, 1, 1, 1, 0xF, data, address)
    ack = deepcopy(dut.wbs_ack_o)
    # Wait for acknowledgment
    count = 0
    while not ack:
        if count > timeout:
            raise TimeoutError("Timeout waiting for write acknowledgment")
        ack, _ = wb_tr(dut, 1, 1, 1, 0xF, data, address)
        count += 1
    # End the transaction
    wb_tr(dut, 0, 0, 0, 0, 0, 0)

def wb_read(dut, address, timeout=1000):
    # Start the transaction
    ack, data = wb_tr(dut, 1, 1, 0, 0xF, 0, address)
    # Wait for acknowledgment
    count = 0
    while not ack:
        if count > timeout:
            raise TimeoutError("Timeout waiting for read acknowledgment")
        ack, data = wb_tr(dut, 1, 1, 0, 0xF, 0, address)
        count += 1
    # If ack is high, advance the simulation by one more tick
    if ack:
        dut.sim_tick()
    # End the transaction
    wb_tr(dut, 0, 0, 0, 0, 0, 0)

    return data
