module Scalar_Register_File
#(
  parameter REG_DEPTH = 32,
  parameter REG_WIDTH = 32,
  parameter ADDR_WIDTH = 5
)
(
  input logic clk, 
  input logic reset, // Reset signal
  input wire [ADDR_WIDTH-1:0] read_address, 
  input wire [ADDR_WIDTH-1:0] write_address, 
  input wire [REG_WIDTH-1:0] write_data, 
  input wire write_enable, 
  output wire [REG_WIDTH-1:0] read_data
);

  // Declare the register file
  reg [REG_WIDTH-1:0] register_file [0:REG_DEPTH-1];

  // Write Operation
  always @(posedge clk or posedge reset) begin // sensitive to reset signal
    if (reset) begin // if reset is asserted
      integer i;
      for(i = 0; i < REG_DEPTH; i = i + 1) begin
        register_file[i] <= 0; // clear all the registers
      end
    end else if (write_enable) begin
      register_file[write_address] <= write_data;
    end
  end

  // Read Operation
  assign read_data = register_file[read_address];

endmodule