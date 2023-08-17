module VectorRegFile_Param (
	clk,
	reset,
	rAddr1_1,
	rAddr2_1,
	rData1,
	rAddr1_2,
	rAddr2_2,
	rData2,
	wAddr1,
	wAddr2,
	wData,
	wEnable
);
	parameter ADDR_WIDTH = 5;
	parameter DATA_WIDTH = 32;
	parameter NUM_REG = 32;
	parameter NUM_ELE = 32;
	input wire clk;
	input wire reset;
	input wire [ADDR_WIDTH - 1:0] rAddr1_1;
	input wire [ADDR_WIDTH - 1:0] rAddr2_1;
	output reg [DATA_WIDTH - 1:0] rData1;
	input wire [ADDR_WIDTH - 1:0] rAddr1_2;
	input wire [ADDR_WIDTH - 1:0] rAddr2_2;
	output reg [DATA_WIDTH - 1:0] rData2;
	input wire [ADDR_WIDTH - 1:0] wAddr1;
	input wire [ADDR_WIDTH - 1:0] wAddr2;
	input wire [DATA_WIDTH - 1:0] wData;
	input wire wEnable;
	reg [DATA_WIDTH - 1:0] reg_file [0:NUM_REG - 1][0:NUM_ELE - 1];
	always @(posedge clk or posedge reset)
		if (reset) begin : sv2v_autoblock_1
			integer i;
			for (i = 0; i < NUM_REG; i = i + 1)
				begin : sv2v_autoblock_2
					integer j;
					for (j = 0; j < NUM_ELE; j = j + 1)
						reg_file[i][j] <= 1'sb0;
				end
		end
		else if (wEnable)
			reg_file[wAddr1][wAddr2] <= wData;
	always @(*) begin
		rData1 = reg_file[rAddr1_1][rAddr2_1];
		rData2 = reg_file[rAddr1_2][rAddr2_2];
	end
endmodulemodule VectorRegFile (
	`ifdef USE_POWER_PINS
    inout wire vccd1,	// User area 1 1.8V supply
    inout wire vssd1,	// User area 1 digital ground
	`endif
	clk,
	reset,
	rAddr1_1,
	rAddr2_1,
	rData1,
	rAddr1_2,
	rAddr2_2,
	rData2,
	wAddr1,
	wAddr2,
	wData,
	wEnable
);

	parameter ADDR_WIDTH = 5;
	parameter DATA_WIDTH = 32;
	parameter NUM_REG = 6;
	parameter NUM_ELE = 32;

	input wire clk;
	input wire reset;
	input wire [ADDR_WIDTH - 1:0] rAddr1_1;
	input wire [ADDR_WIDTH - 1:0] rAddr2_1;
	output reg [DATA_WIDTH - 1:0] rData1;
	input wire [ADDR_WIDTH - 1:0] rAddr1_2;
	input wire [ADDR_WIDTH - 1:0] rAddr2_2;
	output reg [DATA_WIDTH - 1:0] rData2;
	input wire [ADDR_WIDTH - 1:0] wAddr1;
	input wire [ADDR_WIDTH - 1:0] wAddr2;
	input wire [DATA_WIDTH - 1:0] wData;
	input wire wEnable;

	VectorRegFile_Param #(
		.ADDR_WIDTH(ADDR_WIDTH),
		.DATA_WIDTH(DATA_WIDTH),
		.NUM_REG(NUM_REG),
		.NUM_ELE(NUM_ELE)
	) u_VectorRegFile_Param (
		.clk(clk),
		.reset(reset),
		.rAddr1_1(rAddr1_1),
		.rAddr2_1(rAddr2_1),
		.rData1(rData1),
		.rAddr1_2(rAddr1_2),
		.rAddr2_2(rAddr2_2),
		.rData2(rData2),
		.wAddr1(wAddr1),
		.wAddr2(wAddr2),
		.wData(wData),
		.wEnable(wEnable)
	);
endmodule
