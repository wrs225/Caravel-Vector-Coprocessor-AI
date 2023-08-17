module Scalar_Register_File_Param (
	clk,
	reset,
	read_address,
	write_address,
	write_data,
	write_enable,
	read_data
);
	parameter REG_DEPTH = 32;
	parameter REG_WIDTH = 32;
	parameter ADDR_WIDTH = 5;
	input wire clk;
	input wire reset;
	input wire [ADDR_WIDTH - 1:0] read_address;
	input wire [ADDR_WIDTH - 1:0] write_address;
	input wire [REG_WIDTH - 1:0] write_data;
	input wire write_enable;
	output wire [REG_WIDTH - 1:0] read_data;
	reg [REG_WIDTH - 1:0] register_file [0:REG_DEPTH - 1];
	always @(posedge clk or posedge reset)
		if (reset) begin : sv2v_autoblock_1
			integer i;
			for (i = 0; i < REG_DEPTH; i = i + 1)
				register_file[i] <= 0;
		end
		else if (write_enable)
			register_file[write_address] <= write_data;
	assign read_data = register_file[read_address];
endmodule
module Scalar_Register_File (
	clk,
	reset,
	read_address,
	write_address,
	write_data,
	write_enable,
	read_data
);
	parameter REG_DEPTH = 6;
	parameter REG_WIDTH = 32;
	parameter ADDR_WIDTH = 5;
	input wire clk;
	input wire reset;
	input wire [ADDR_WIDTH - 1:0] read_address;
	input wire [ADDR_WIDTH - 1:0] write_address;
	input wire [REG_WIDTH - 1:0] write_data;
	input wire write_enable;
	output wire [REG_WIDTH - 1:0] read_data;

	Scalar_Register_File_Param #(
		.REG_DEPTH(REG_DEPTH),
		.REG_WIDTH(REG_WIDTH),
		.ADDR_WIDTH(ADDR_WIDTH)
	) srfp (
		.clk(clk),
		.reset(reset),
		.read_address(read_address),
		.write_address(write_address),
		.write_data(write_data),
		.write_enable(write_enable),
		.read_data(read_data)
	);
endmodule