module VectorRegFile #(parameter ADDR_WIDTH = 5, DATA_WIDTH = 32, NUM_REG = 32, NUM_ELE = 32)(
  input logic clk,
  input logic reset_n,
  // Read Ports
  input logic [ADDR_WIDTH-1:0] rAddr1_1, rAddr2_1, // Reading vector and element address for port 1
  output logic [DATA_WIDTH-1:0] rData1,
  input logic [ADDR_WIDTH-1:0] rAddr1_2, rAddr2_2, // Reading vector and element address for port 2
  output logic [DATA_WIDTH-1:0] rData2,
  // Write Ports
  input logic [ADDR_WIDTH-1:0] wAddr1, wAddr2, // Writing vector and element address
  input logic [DATA_WIDTH-1:0] wData,
  input logic wEnable
);

  // The vector register file
  logic [DATA_WIDTH-1:0] reg_file [0:NUM_REG-1][0:NUM_ELE-1];

  always_ff @(posedge clk or negedge reset_n) begin
    if (!reset_n) begin
      // Clear all the registers on reset
      for (integer i = 0; i < NUM_REG; i = i + 1) 
        for (integer j = 0; j < NUM_ELE; j = j + 1) 
          reg_file[i][j] <= '0;
    end else if(wEnable) begin
      // Write the data at write address if write enable is high
      reg_file[wAddr1][wAddr2] <= wData;
    end
  end

  always_comb begin
    // Read the data from the read addresses
    rData1 = reg_file[rAddr1_1][rAddr2_1];
    rData2 = reg_file[rAddr1_2][rAddr2_2];
  end
endmodule