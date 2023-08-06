`include "../../UtilityBlocks/sim/WishboneStream.v"
`include "../../Dpath/sim/TopModule.v"
module WrapperBlock (
    input wb_clk_i,
    input wb_rst_i,
    input wbs_stb_i,
    input wbs_cyc_i,
    input wbs_we_i,
    input [3:0] wbs_sel_i,
    input [31:0] wbs_dat_i,
    input [31:0] wbs_adr_i,
    output logic wbs_ack_o,
    output [31:0] wbs_dat_o,
    input logic clk,
    input logic reset
);

    // Internal signals
    logic [63:0] load_recv_msg_internal;
    logic load_recv_val_internal;
    logic load_recv_rdy_internal;
    logic [31:0] instruction_recv_msg_internal;
    logic instruction_recv_val_internal;
    logic instruction_recv_rdy_internal;
    logic [31:0] store_send_msg_internal;
    logic store_send_val_internal;
    logic store_send_rdy_internal;

    // Instance of wb_converter
    wb_converter wb_converter_inst (
        .wb_clk_i(clk),  // Modified connection
        .wb_rst_i(wb_rst_i),
        .wbs_stb_i(wbs_stb_i),
        .wbs_cyc_i(wbs_cyc_i),
        .wbs_we_i(wbs_we_i),
        .wbs_sel_i(wbs_sel_i),
        .wbs_dat_i(wbs_dat_i),
        .wbs_adr_i(wbs_adr_i),
        .wbs_ack_o(wbs_ack_o),
        .wbs_dat_o(wbs_dat_o),
        .load_recv_msg(load_recv_msg_internal),
        .load_recv_val(load_recv_val_internal),
        .load_recv_rdy(load_recv_rdy_internal),
        .instruction_recv_msg(instruction_recv_msg_internal),
        .instruction_recv_val(instruction_recv_val_internal),
        .instruction_recv_rdy(instruction_recv_rdy_internal),
        .store_send_msg(store_send_msg_internal),
        .store_send_val(store_send_val_internal),
        .store_send_rdy(store_send_rdy_internal)
    );

    // Instance of TopModule
    TopModule TopModule_inst (
        .clk(clk),
        .reset(reset),
        .load_recv_msg(load_recv_msg_internal),
        .load_recv_val(load_recv_val_internal),
        .load_recv_rdy(load_recv_rdy_internal),
        .instruction_recv_msg(instruction_recv_msg_internal),
        .instruction_recv_val(instruction_recv_val_internal),
        .instruction_recv_rdy(instruction_recv_rdy_internal),
        .store_send_msg(store_send_msg_internal),
        .store_send_val(store_send_val_internal),
        .store_send_rdy(store_send_rdy_internal)
    );

endmodule
