module Predicate_Register_File
    #(parameter ADDR_WIDTH = 5, DATA_WIDTH = 1, NUM_REGISTERS = 32)
    (
        input logic clk,
        input logic reset,
        input logic [ADDR_WIDTH-1:0] read_addr1, read_addr2,
        input logic [ADDR_WIDTH-1:0] write_addr1, write_addr2,
        input logic write_enable,
        output logic [DATA_WIDTH-1:0] data_out,
        input logic [DATA_WIDTH-1:0] data_in
    );

    // Declare register file
    logic [DATA_WIDTH-1:0] register_file [0:NUM_REGISTERS-1][0:NUM_REGISTERS-1];

    // Read operation
    always_comb begin
        data_out = register_file[read_addr1][read_addr2];
    end

    // Write operation
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            for (int i = 0; i < NUM_REGISTERS; i++) 
                for (int j = 0; j < NUM_REGISTERS; j++)
                    register_file[i][j] <= 0;
        end
        else if (write_enable) begin
            register_file[write_addr1][write_addr2] <= data_in;
        end
    end
endmodule
