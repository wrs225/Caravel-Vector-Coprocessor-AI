module wb_converter (
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

    output logic [63:0] load_recv_msg,
    output logic load_recv_val,
    input load_recv_rdy,

    output logic [31:0] instruction_recv_msg,
    output logic instruction_recv_val,
    input instruction_recv_rdy,

    input [31:0] store_send_msg,
    input store_send_val,
    output logic store_send_rdy
);

    // Internal signals
    logic [31:0] internal_wbs_dat_i;
    logic [31:0] internal_wbs_adr_i;
    logic store_transaction_in_progress;

    assign internal_wbs_dat_i = (wbs_stb_i && wbs_cyc_i) ? wbs_dat_i : 32'b0;
    assign internal_wbs_adr_i = (wbs_stb_i && wbs_cyc_i) ? wbs_adr_i : 32'b0;

    assign wbs_ack_o = wbs_cyc_i && wbs_stb_i && 
                       ((internal_wbs_adr_i == 32'h30000000 && instruction_recv_rdy) || 
                       ((internal_wbs_adr_i > 32'h30000000) && (!wbs_we_i && store_send_val && store_send_rdy && store_transaction_in_progress)) ||
                       ((internal_wbs_adr_i > 32'h30000000) && wbs_we_i && load_recv_rdy && instruction_recv_rdy));
    assign store_send_rdy = !wbs_we_i && wbs_cyc_i && wbs_stb_i && (internal_wbs_adr_i > 32'h30000000);
    assign wbs_dat_o = store_send_msg;

    always_ff @(posedge wb_clk_i or posedge wb_rst_i) begin
        if (wb_rst_i) begin
            store_transaction_in_progress <= 0;
        end else if (wbs_ack_o) begin
            store_transaction_in_progress <= 0;
        end else if (instruction_recv_val && load_recv_val && (internal_wbs_adr_i > 32'h30000000) && (!wbs_we_i)) begin
            store_transaction_in_progress <= 1;
        end
    end

    always_comb begin
        // Default values
        load_recv_msg = 64'b0;
        load_recv_val = 0;
        instruction_recv_msg = 32'b0;
        instruction_recv_val = 0;

        if (!store_transaction_in_progress) begin
            if (internal_wbs_adr_i == 32'h30000000) begin
                // Send instruction to processor
                instruction_recv_msg = internal_wbs_dat_i;
                instruction_recv_val = wbs_cyc_i && wbs_stb_i;
            end else if (internal_wbs_adr_i > 32'h30000000) begin
                // Send load/store instruction and data to processor
                load_recv_msg = {(internal_wbs_adr_i - 32'h30000004) >> 2, internal_wbs_dat_i};
                load_recv_val = wbs_cyc_i && wbs_stb_i;
                if (wbs_we_i) begin
                    // Load operation
                    instruction_recv_msg = {5'b00000, 27'b0};
                end else begin
                    // Store operation
                    instruction_recv_msg = {5'b00001, 27'b0};
                end
                instruction_recv_val = wbs_cyc_i && wbs_stb_i;
            end
        end
    end

endmodule
