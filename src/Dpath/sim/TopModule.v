//Filepaths added by humans
`include "./queue.v"
`include "./Counter.v"
`include "./Decoder.v"
`include "../../RegisterFiles/sim/VectorRegFile.v"
`include "./ALU.v"
module TopModule (
    input logic clk,
    input logic reset,

    // Receive interface for load_queue
    input logic [63:0] load_recv_msg,
    input logic load_recv_val,
    output logic load_recv_rdy,

    // Receive interface for instruction_queue
    input logic [31:0] instruction_recv_msg,
    input logic instruction_recv_val,
    output logic instruction_recv_rdy,

    // Send interface for store_queue
    output logic [31:0] store_send_msg,
    output logic store_send_val,
    input logic store_send_rdy
);

    // Internal signals for send interface of load_queue and instruction_queue
    logic [63:0] load_send_msg;
    logic load_send_val;
    logic load_send_rdy;

    logic [31:0] instruction_send_msg;
    logic instruction_send_val;
    logic instruction_send_rdy;

    // Internal signals for receive interface of store_queue
    logic [31:0] store_recv_msg;
    logic store_recv_val;
    logic store_recv_rdy;

    // Internal signals for Decoder
    logic clock_enable;
    logic clock_bypass;
    logic [4:0] vector_reg_write_select;
    logic [4:0] reg_file_addr1;
    logic [4:0] reg_file_addr2;
    logic mux_bit;
    logic vector_reg_write_bit;
    logic predicate_reg_write_bit;
    logic scalar_reg_write_bit;
    logic vector_reg_load_mux_bit;
    logic scalar_reg_load_mux_bit;
    logic [2:0] functional_unit_mux_bit;
    logic add_subtract_bit;
    logic load_store_bit;
    logic [1:0] bitwise_op_select;
    logic [1:0] predicate_op_select;

    // Internal signals for VectorRegFile
    logic [31:0] wb_addr;
    logic [31:0] wb_data;
    logic [31:0] rData1;
    logic [31:0] rData2;

    // New wire for functional_unit_output_mux
    logic [31:0] functional_unit_output_mux;

    // Mux output for VectorRegFile wData
    logic [31:0] wData_mux_out;

    // Mux outputs for VectorRegFile wAddr1 and wAddr2
    logic [4:0] wAddr1_mux_out;
    logic [4:0] wAddr2_mux_out;

    // 2-input muxes for VectorRegFile rAddr1_1 and rAddr2_1
    logic [4:0] rAddr1_1_mux_out;
    logic [4:0] rAddr2_1_mux_out;

    // Instantiate load_queue
    queue #(.WIDTH(64), .DEPTH(16)) load_queue (
        .clk(clk),
        .reset(reset),
        .recv_msg(load_recv_msg),
        .recv_val(load_recv_val),
        .recv_rdy(load_recv_rdy),
        .send_msg(load_send_msg),
        .send_val(load_send_val),
        .send_rdy(load_send_rdy)
    );

    // Instantiate instruction_queue
    queue #(.WIDTH(32), .DEPTH(16)) instruction_queue (
        .clk(clk),
        .reset(reset),
        .recv_msg(instruction_recv_msg),
        .recv_val(instruction_recv_val),
        .recv_rdy(instruction_recv_rdy),
        .send_msg(instruction_send_msg),
        .send_val(instruction_send_val),
        .send_rdy(instruction_send_rdy)
    );

    // Instantiate store_queue
    queue #(.WIDTH(32), .DEPTH(16)) store_queue (
        .clk(clk),
        .reset(reset),
        .recv_msg(store_recv_msg),
        .recv_val(store_recv_val),
        .recv_rdy(store_recv_rdy),
        .send_msg(store_send_msg),
        .send_val(store_send_val),
        .send_rdy(store_send_rdy)
    );

    // Instantiate Decoder
    Decoder decoder (
        .instruction(instruction_send_msg),
        .instruction_valid(instruction_send_val),
        .reg_file_addr1(reg_file_addr1),
        .reg_file_addr2(reg_file_addr2),
        .mux_bit(mux_bit),
        .vector_reg_write_bit(vector_reg_write_bit),
        .predicate_reg_write_bit(predicate_reg_write_bit),
        .scalar_reg_write_bit(scalar_reg_write_bit),
        .vector_reg_load_mux_bit(vector_reg_load_mux_bit),
        .scalar_reg_load_mux_bit(scalar_reg_load_mux_bit),
        .functional_unit_mux_bit(functional_unit_mux_bit),
        .add_subtract_bit(add_subtract_bit),
        .load_store_bit(load_store_bit),
        .clock_enable(clock_enable),
        .clock_bypass(clock_bypass),
        .bitwise_op_select(bitwise_op_select),
        .predicate_op_select(predicate_op_select),
        .vector_reg_write_select(vector_reg_write_select)
    );

    // Internal signal for Counter
    logic [4:0] counter;
    logic done;

    // Instantiate Counter
    Counter #(.WIDTH(5), .COUNTER_MAX(2**5-1)) counter_module (
        .clk(clk),
        .enable(clock_enable),
        .reset(reset),
        .counter(counter),
        .done(done)
    );

    // OR the done output with clock_bypass and connect this result to instruction_send_rdy
    assign instruction_send_rdy = done | clock_bypass;

    // Create new wires for wb_addr and wb_data
    assign wb_addr = load_recv_msg[63:32];
    assign wb_data = load_recv_msg[31:0];

    // 2-input mux for VectorRegFile wData
    assign wData_mux_out = load_store_bit ? wb_data : functional_unit_output_mux;

    // 2-input muxes for VectorRegFile wAddr1 and wAddr2
    assign wAddr1_mux_out = load_store_bit ? wb_addr[9:5] : vector_reg_write_select;
    assign wAddr2_mux_out = load_store_bit ? wb_addr[4:0] : counter;

    // 2-input muxes for VectorRegFile rAddr1_1 and rAddr2_1
    assign rAddr1_1_mux_out = load_store_bit ? wb_addr[9:5] : reg_file_addr1;
    assign rAddr2_1_mux_out = load_store_bit ? wb_addr[4:0] : counter;

    // Instantiate VectorRegFile
    VectorRegFile #(.ADDR_WIDTH(5), .DATA_WIDTH(32), .NUM_REG(32), .NUM_ELE(32)) reg_file (
        .clk(clk),
        .reset_n(~reset),
        .rAddr1_1(rAddr1_1_mux_out),
        .rAddr2_1(rAddr2_1_mux_out),
        .rData1(rData1),
        .rAddr1_2(reg_file_addr2),
        .rAddr2_2(counter),
        .rData2(rData2),
        .wAddr1(wAddr1_mux_out),
        .wAddr2(wAddr2_mux_out),
        .wData(wData_mux_out),
        .wEnable(vector_reg_write_bit)
    );

    // Instantiate ALU
    ALU #(32) alu (
        .A(rData1),
        .B(rData2),
        .C(wb_data),
        .AddSub(add_subtract_bit),
        .muxControl(mux_bit),
        .outputControl(functional_unit_mux_bit),
        .bitwiseControl(bitwise_op_select),
        .compControl(predicate_op_select),
        .finalResult(functional_unit_output_mux),
        .predicate(predicate_reg_write_bit)
    );

    // Corrected line
    assign store_recv_msg = rData1;
    assign store_recv_val = load_store_bit & !vector_reg_write_bit;

    // Corrected line
    assign load_send_rdy = load_store_bit;

endmodule
