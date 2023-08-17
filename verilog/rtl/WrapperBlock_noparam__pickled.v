module wb_converter (
	wb_clk_i,
	wb_rst_i,
	wbs_stb_i,
	wbs_cyc_i,
	wbs_we_i,
	wbs_sel_i,
	wbs_dat_i,
	wbs_adr_i,
	wbs_ack_o,
	wbs_dat_o,
	load_recv_msg,
	load_recv_val,
	load_recv_rdy,
	instruction_recv_msg,
	instruction_recv_val,
	instruction_recv_rdy,
	store_send_msg,
	store_send_val,
	store_send_rdy
);
	input wb_clk_i;
	input wb_rst_i;
	input wbs_stb_i;
	input wbs_cyc_i;
	input wbs_we_i;
	input [3:0] wbs_sel_i;
	input [31:0] wbs_dat_i;
	input [31:0] wbs_adr_i;
	output wire wbs_ack_o;
	output wire [31:0] wbs_dat_o;
	output reg [63:0] load_recv_msg;
	output reg load_recv_val;
	input load_recv_rdy;
	output reg [31:0] instruction_recv_msg;
	output reg instruction_recv_val;
	input instruction_recv_rdy;
	input [31:0] store_send_msg;
	input store_send_val;
	output wire store_send_rdy;
	wire [31:0] internal_wbs_dat_i;
	wire [31:0] internal_wbs_adr_i;
	reg store_transaction_in_progress;
	assign internal_wbs_dat_i = (wbs_stb_i && wbs_cyc_i ? wbs_dat_i : 32'b00000000000000000000000000000000);
	assign internal_wbs_adr_i = (wbs_stb_i && wbs_cyc_i ? wbs_adr_i : 32'b00000000000000000000000000000000);
	assign wbs_ack_o = (wbs_cyc_i && wbs_stb_i) && ((((internal_wbs_adr_i == 32'h30000000) && instruction_recv_rdy) || ((internal_wbs_adr_i > 32'h30000000) && (((!wbs_we_i && store_send_val) && store_send_rdy) && store_transaction_in_progress))) || ((((internal_wbs_adr_i > 32'h30000000) && wbs_we_i) && load_recv_rdy) && instruction_recv_rdy));
	assign store_send_rdy = ((!wbs_we_i && wbs_cyc_i) && wbs_stb_i) && (internal_wbs_adr_i > 32'h30000000);
	assign wbs_dat_o = store_send_msg;
	always @(posedge wb_clk_i or posedge wb_rst_i)
		if (wb_rst_i)
			store_transaction_in_progress <= 0;
		else if (wbs_ack_o)
			store_transaction_in_progress <= 0;
		else if (((instruction_recv_val && load_recv_val) && (internal_wbs_adr_i > 32'h30000000)) && !wbs_we_i)
			store_transaction_in_progress <= 1;
	always @(*) begin
		load_recv_msg = 64'b0000000000000000000000000000000000000000000000000000000000000000;
		load_recv_val = 0;
		instruction_recv_msg = 32'b00000000000000000000000000000000;
		instruction_recv_val = 0;
		if (!store_transaction_in_progress) begin
			if (internal_wbs_adr_i == 32'h30000000) begin
				instruction_recv_msg = internal_wbs_dat_i;
				instruction_recv_val = wbs_cyc_i && wbs_stb_i;
			end
			else if (internal_wbs_adr_i > 32'h30000000) begin
				load_recv_msg = {(internal_wbs_adr_i - 32'h30000004) >> 2, internal_wbs_dat_i};
				load_recv_val = wbs_cyc_i && wbs_stb_i;
				if (wbs_we_i)
					instruction_recv_msg = 32'b00000000000000000000000000000000;
				else
					instruction_recv_msg = 32'b00001000000000000000000000000000;
				instruction_recv_val = wbs_cyc_i && wbs_stb_i;
			end
		end
	end
endmodule
module queue (
	clk,
	reset,
	recv_msg,
	recv_val,
	recv_rdy,
	send_msg,
	send_val,
	send_rdy
);
	parameter WIDTH = 8;
	parameter DEPTH = 16;
	input wire clk;
	input wire reset;
	input wire [WIDTH - 1:0] recv_msg;
	input wire recv_val;
	output wire recv_rdy;
	output wire [WIDTH - 1:0] send_msg;
	output wire send_val;
	input wire send_rdy;
	reg [WIDTH - 1:0] queue [0:DEPTH - 1];
	reg [$clog2(DEPTH) - 1:0] head;
	reg [$clog2(DEPTH) - 1:0] tail;
	reg full;
	reg empty;
	reg next_full;
	reg next_empty;
	always @(posedge clk or posedge reset)
		if (reset) begin
			head <= 0;
			tail <= 0;
			full <= 0;
			empty <= 1;
		end
		else begin
			head <= ((send_rdy && send_val) && !empty ? (head == (DEPTH - 1) ? 0 : head + 1) : head);
			tail <= ((recv_rdy && recv_val) && !full ? (tail == (DEPTH - 1) ? 0 : tail + 1) : tail);
			full <= next_full;
			empty <= next_empty;
		end
	always @(posedge clk or posedge reset)
		if (reset) begin : sv2v_autoblock_1
			reg signed [31:0] i;
			for (i = 0; i < DEPTH; i = i + 1)
				queue[i] <= 1'sb0;
		end
		else if ((recv_rdy && recv_val) && !full)
			queue[tail] <= recv_msg;
	always @(*) begin
		next_full = full;
		next_empty = empty;
		if ((recv_rdy && recv_val) && !full) begin
			if ((send_rdy && send_val) && !empty)
				;
			else begin
				next_full = (tail == (DEPTH - 1) ? 0 : tail + 1) == head;
				next_empty = 0;
			end
		end
		else if ((send_rdy && send_val) && !empty) begin
			next_empty = (head == (DEPTH - 1) ? 0 : head + 1) == tail;
			next_full = 0;
		end
	end
	assign recv_rdy = !full;
	assign send_val = !empty;
	assign send_msg = queue[head];
endmodule
module Counter (
	clk,
	enable,
	reset,
	counter,
	done
);
	parameter WIDTH = 4;
	parameter COUNTER_MAX = (2 ** WIDTH) - 1;
	input wire clk;
	input wire enable;
	input wire reset;
	output reg [WIDTH - 1:0] counter;
	output wire done;
	always @(posedge clk or posedge reset)
		if (reset)
			counter <= 0;
		else if (enable)
			counter <= counter + 1;
	assign done = (counter == COUNTER_MAX ? 1'b1 : 1'b0);
endmodule
module Decoder (
	instruction,
	instruction_valid,
	reg_file_addr1,
	reg_file_addr2,
	mux_bit,
	vector_reg_write_bit,
	predicate_reg_write_bit,
	scalar_reg_write_bit,
	vector_reg_load_mux_bit,
	scalar_reg_load_mux_bit,
	functional_unit_mux_bit,
	add_subtract_bit,
	load_store_bit,
	clock_enable,
	clock_bypass,
	bitwise_op_select,
	predicate_op_select,
	vector_reg_write_select
);
	input wire [31:0] instruction;
	input wire instruction_valid;
	output reg [4:0] reg_file_addr1;
	output reg [4:0] reg_file_addr2;
	output reg mux_bit;
	output reg vector_reg_write_bit;
	output reg predicate_reg_write_bit;
	output reg scalar_reg_write_bit;
	output reg vector_reg_load_mux_bit;
	output reg scalar_reg_load_mux_bit;
	output reg [2:0] functional_unit_mux_bit;
	output reg add_subtract_bit;
	output reg load_store_bit;
	output reg clock_enable;
	output reg clock_bypass;
	output reg [1:0] bitwise_op_select;
	output reg [3:0] predicate_op_select;
	output reg [4:0] vector_reg_write_select;
	reg [4:0] opcode;
	always @(*)
		if (instruction_valid == 1'b0) begin
			reg_file_addr1 = 5'b00000;
			reg_file_addr2 = 5'b00000;
			mux_bit = 1'b0;
			vector_reg_write_bit = 1'b0;
			predicate_reg_write_bit = 1'b0;
			scalar_reg_write_bit = 1'b0;
			vector_reg_load_mux_bit = 1'b0;
			scalar_reg_load_mux_bit = 1'b0;
			functional_unit_mux_bit = 3'b000;
			add_subtract_bit = 1'b0;
			load_store_bit = 1'b0;
			clock_enable = 1'b0;
			clock_bypass = 1'b1;
			bitwise_op_select = 2'b00;
			predicate_op_select = 4'b0000;
			vector_reg_write_select = 5'b00000;
		end
		else begin
			reg_file_addr1 = instruction[20:16];
			reg_file_addr2 = instruction[15:11];
			vector_reg_write_select = instruction[25:21];
			opcode = instruction[31:27];
			case (opcode)
				5'b00000, 5'b00001: begin
					clock_bypass = 1;
					clock_enable = 0;
					mux_bit = 0;
					vector_reg_write_bit = (opcode == 5'b00000 ? 1 : 0);
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 0;
					add_subtract_bit = 0;
					load_store_bit = 1;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				5'b00010, 5'b00011, 5'b00110: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = (opcode == 5'b00110 ? 1 : 0);
					vector_reg_write_bit = 1;
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 0;
					add_subtract_bit = (opcode == 5'b00011 ? 1 : 0);
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				5'b00100, 5'b00101: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = (opcode == 5'b00101 ? 1 : 0);
					vector_reg_write_bit = 1;
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 2;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				5'b00111, 5'b10000: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 1;
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 1;
					add_subtract_bit = (opcode == 5'b10000 ? 1 : 0);
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				5'b01000: begin
					clock_enable = 1;
					vector_reg_write_bit = 1;
					functional_unit_mux_bit = 3'b011;
					mux_bit = 0;
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					add_subtract_bit = 0;
					load_store_bit = 0;
					clock_bypass = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				5'b01001, 5'b01010, 5'b01011: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 1;
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 4;
					add_subtract_bit = 0;
					load_store_bit = 0;
					if (opcode == 5'b01001)
						bitwise_op_select = 2'b00;
					else if (opcode == 5'b01010)
						bitwise_op_select = 2'b01;
					else if (opcode == 5'b01011)
						bitwise_op_select = 2'b10;
					predicate_op_select = 4'b0000;
				end
				5'b01100: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				5'b01101: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0001;
				end
				5'b01110: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0010;
				end
				5'b01111: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0011;
				end
				5'b11000: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0100;
				end
				5'b10001: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0101;
				end
				5'b10010: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0110;
				end
				5'b10100: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0111;
				end
				5'b10111: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 0;
					vector_reg_write_bit = 0;
					predicate_reg_write_bit = 1;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 5;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b1000;
				end
				5'b10101: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 1;
					vector_reg_write_bit = 1;
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 3'b011;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				5'b10110: begin
					clock_bypass = 0;
					clock_enable = 1;
					mux_bit = 1;
					vector_reg_write_bit = 1;
					predicate_reg_write_bit = 0;
					scalar_reg_write_bit = 0;
					vector_reg_load_mux_bit = 0;
					scalar_reg_load_mux_bit = 0;
					functional_unit_mux_bit = 1;
					add_subtract_bit = 0;
					load_store_bit = 0;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
				end
				default: begin
					reg_file_addr1 = 5'b00000;
					reg_file_addr2 = 5'b00000;
					mux_bit = 1'b0;
					vector_reg_write_bit = 1'b0;
					predicate_reg_write_bit = 1'b0;
					scalar_reg_write_bit = 1'b0;
					vector_reg_load_mux_bit = 1'b0;
					scalar_reg_load_mux_bit = 1'b0;
					functional_unit_mux_bit = 3'b000;
					add_subtract_bit = 1'b0;
					load_store_bit = 1'b0;
					clock_enable = 1'b0;
					clock_bypass = 1'b1;
					bitwise_op_select = 2'b00;
					predicate_op_select = 4'b0000;
					vector_reg_write_select = 5'b00000;
				end
			endcase
		end
endmodule
//Removed VectorRegFile from here to put in blackbox file.
module Multiplier (
	A,
	B,
	Result
);
	parameter WIDTH = 32;
	input wire [WIDTH - 1:0] A;
	input wire [WIDTH - 1:0] B;
	output reg [WIDTH - 1:0] Result;
	always @(*) Result = A * B;
endmodule
module AddSub (
	A,
	B,
	AddSub,
	Result
);
	parameter WIDTH = 32;
	input wire [WIDTH - 1:0] A;
	input wire [WIDTH - 1:0] B;
	input wire AddSub;
	output reg [WIDTH - 1:0] Result;
	always @(*)
		if (AddSub == 0)
			Result = A + B;
		else
			Result = A - B;
endmodule
module fp_addsub (
	a,
	b,
	subtract,
	y
);
	input wire [31:0] a;
	input wire [31:0] b;
	input wire subtract;
	output reg [31:0] y;
	wire [31:0] b_neg;
	reg a_sign;
	reg b_sign;
	reg [7:0] a_exp;
	reg [7:0] b_exp;
	reg [23:0] a_frac;
	reg [23:0] b_frac;
	reg y_sign;
	reg [7:0] y_exp;
	reg [23:0] y_frac;
	reg [47:0] y_frac_intermediate;
	reg [7:0] y_exp_intermediate;
	reg [5:0] shift_amount;
	assign b_neg = (subtract ? {b[31] ^ 1'b1, b[30:0]} : b);
	function automatic [5:0] priority_encoder;
		input [47:0] in;
		integer i;
		reg [0:1] _sv2v_jump;
		begin
			_sv2v_jump = 2'b00;
			begin : sv2v_autoblock_1
				integer _sv2v_value_on_break;
				for (i = 47; i >= 0; i = i - 1)
					if (_sv2v_jump < 2'b10) begin
						_sv2v_jump = 2'b00;
						if (in[i]) begin
							priority_encoder = 23 - i;
							_sv2v_jump = 2'b11;
						end
						_sv2v_value_on_break = i;
					end
				if (!(_sv2v_jump < 2'b10))
					i = _sv2v_value_on_break;
				if (_sv2v_jump != 2'b11)
					_sv2v_jump = 2'b00;
			end
			if (_sv2v_jump == 2'b00) begin
				priority_encoder = 6'b000000;
				_sv2v_jump = 2'b11;
			end
		end
	endfunction
	always @(*) begin
		a_sign = a[31];
		b_sign = b_neg[31];
		a_exp = a[30:23];
		b_exp = b_neg[30:23];
		a_frac = {1'b1, a[22:0]};
		b_frac = {1'b1, b_neg[22:0]};
		if (a_exp > b_exp) begin
			y_exp_intermediate = a_exp;
			if (b_sign ^ a_sign)
				y_frac_intermediate = a_frac - (b_frac >> (a_exp - b_exp));
			else
				y_frac_intermediate = a_frac + (b_frac >> (a_exp - b_exp));
			y_sign = a_sign;
		end
		else if (a_exp < b_exp) begin
			y_exp_intermediate = b_exp;
			if (b_sign ^ a_sign)
				y_frac_intermediate = b_frac - (a_frac >> (b_exp - a_exp));
			else
				y_frac_intermediate = (a_frac >> (b_exp - a_exp)) + b_frac;
			y_sign = b_sign;
		end
		else begin
			y_exp_intermediate = a_exp;
			if (a_frac >= b_frac) begin
				if (b_sign ^ a_sign)
					y_frac_intermediate = a_frac - b_frac;
				else
					y_frac_intermediate = a_frac + b_frac;
				y_sign = a_sign;
			end
			else begin
				if (b_sign ^ a_sign)
					y_frac_intermediate = b_frac - a_frac;
				else
					y_frac_intermediate = b_frac + a_frac;
				y_sign = b_sign;
			end
		end
		if ((a == 32'b00000000000000000000000000000000) && (b == 32'b00000000000000000000000000000000))
			shift_amount = 6'b000000;
		else
			shift_amount = (y_frac_intermediate[47] ? 6'b000000 : priority_encoder(y_frac_intermediate));
		if (shift_amount[5])
			y_frac = y_frac_intermediate >> -shift_amount;
		else
			y_frac = y_frac_intermediate << shift_amount;
		y_exp = y_exp_intermediate - {{2 {shift_amount[5]}}, shift_amount};
	end
	always @(*)
		if (((a[30:23] == 8'hff) && (a[22:0] == 23'b00000000000000000000000)) && ((b_neg[30:23] == 8'hff) && (b_neg[22:0] == 23'b00000000000000000000000))) begin
			if (subtract && (a_sign ^ b_sign))
				y = 32'h7fc00000;
			else if (a_sign ^ b_sign)
				y = {a_sign, 31'h7f800000};
			else
				y = {y_sign, y_exp, y_frac[22:0]};
		end
		else if (((a[30:23] == 8'hff) && (a[22:0] == 23'b00000000000000000000000)) || ((b_neg[30:23] == 8'hff) && (b_neg[22:0] == 23'b00000000000000000000000)))
			y = {a_sign | b_sign, 31'h7f800000};
		else if (y_frac_intermediate == 48'b000000000000000000000000000000000000000000000000)
			y = 32'b00000000000000000000000000000000;
		else
			y = {y_sign, y_exp, y_frac[22:0]};
endmodule
module fp_multiplier (
	a,
	b,
	y
);
	input wire [31:0] a;
	input wire [31:0] b;
	output wire [31:0] y;
	wire [8:0] a_exponent;
	wire [8:0] b_exponent;
	wire [8:0] y_exponent_temp;
	reg [7:0] y_exponent;
	wire [23:0] a_mantissa;
	wire [23:0] b_mantissa;
	wire [47:0] mult_result;
	wire [22:0] y_mantissa_temp;
	reg [22:0] y_mantissa;
	wire a_sign;
	wire b_sign;
	wire y_sign;
	wire sticky_bit;
	wire r;
	assign a_sign = a[31];
	assign a_exponent = {1'b0, a[30:23]};
	assign a_mantissa = {1'b1, a[22:0]};
	assign b_sign = b[31];
	assign b_exponent = {1'b0, b[30:23]};
	assign b_mantissa = {1'b1, b[22:0]};
	assign y_sign = a_sign ^ b_sign;
	assign mult_result = a_mantissa * b_mantissa;
	assign y_exponent_temp = ((a_exponent + b_exponent) - 127) + mult_result[47];
	assign y_mantissa_temp = (mult_result[47] ? mult_result[46:24] : mult_result[45:23]);
	assign sticky_bit = (mult_result[47] ? |mult_result[22:0] : |mult_result[21:0]);
	assign r = (mult_result[47] ? mult_result[23] : mult_result[22]);
	always @(*)
		if (((a_exponent[7:0] == 8'hff) && (a_mantissa[22:0] != 0)) || ((b_exponent[7:0] == 8'hff) && (b_mantissa[22:0] != 0))) begin
			y_exponent = 8'hff;
			y_mantissa = 23'h400000;
		end
		else if ((((a == 32'b00000000000000000000000000000000) && (b_exponent[7:0] == 8'hff)) && (b_mantissa[22:0] == 0)) || (((b == 32'b00000000000000000000000000000000) && (a_exponent[7:0] == 8'hff)) && (a_mantissa[22:0] == 0))) begin
			y_exponent = 8'hff;
			y_mantissa = 23'h400000;
		end
		else if ((a == 32'b00000000000000000000000000000000) || (b == 32'b00000000000000000000000000000000)) begin
			y_exponent = 8'h00;
			y_mantissa = 23'h000000;
		end
		else if (y_exponent_temp[8]) begin
			y_exponent = 8'hff;
			y_mantissa = 23'h000000;
		end
		else if (((a_exponent[7:0] == 8'hff) && (a_mantissa[22:0] == 0)) && ((b_exponent[7:0] == 8'hff) && (b_mantissa[22:0] == 0))) begin
			y_exponent = 8'hff;
			y_mantissa = 23'h000000;
		end
		else if ((a_exponent + b_exponent) == 0) begin
			y_exponent = 0;
			y_mantissa = y_mantissa_temp >> -y_exponent_temp;
		end
		else begin
			y_exponent = y_exponent_temp[7:0];
			y_mantissa = y_mantissa_temp + (r & sticky_bit);
		end
	assign y = {y_sign, y_exponent, y_mantissa};
endmodule
module BitwiseOperationUnit (
	operandA,
	operandB,
	control,
	result
);
	input [31:0] operandA;
	input [31:0] operandB;
	input [1:0] control;
	output wire [31:0] result;
	reg [31:0] result_reg;
	always @(*)
		case (control)
			2'b00: result_reg = operandA & operandB;
			2'b01: result_reg = operandA | operandB;
			2'b10: result_reg = operandA ^ operandB;
			default: result_reg = 32'b00000000000000000000000000000000;
		endcase
	assign result = result_reg;
endmodule
module comparison_unit (
	in1,
	in2,
	control,
	predicate
);
	parameter WIDTH = 32;
	input wire [WIDTH - 1:0] in1;
	input wire [WIDTH - 1:0] in2;
	input wire [3:0] control;
	output reg predicate;
	always @(*)
		case (control)
			4'b0000: predicate = in1 == 0;
			4'b0001: predicate = in1 != 0;
			4'b0010: predicate = 1;
			4'b0011: predicate = $signed(in1) >= $signed(in2);
			4'b0100: predicate = $signed(in1) < $signed(in2);
			4'b0101: predicate = in1 >= in2;
			4'b0110: predicate = in1 < in2;
			4'b0111: predicate = in1 == in2;
			4'b1000: predicate = in1 != in2;
			default: predicate = 0;
		endcase
endmodule
module ALU (
	A,
	B,
	C,
	AddSub,
	muxControl,
	outputControl,
	bitwiseControl,
	compControl,
	finalResult,
	predicate
);
	parameter WIDTH = 32;
	input wire [WIDTH - 1:0] A;
	input wire [WIDTH - 1:0] B;
	input wire [WIDTH - 1:0] C;
	input wire AddSub;
	input wire muxControl;
	input wire [2:0] outputControl;
	input wire [1:0] bitwiseControl;
	input wire [3:0] compControl;
	output reg [WIDTH - 1:0] finalResult;
	output wire predicate;
	wire [WIDTH - 1:0] muxOut;
	wire [WIDTH - 1:0] multResult;
	wire [WIDTH - 1:0] addSubResult;
	wire [WIDTH - 1:0] fpAddResult;
	wire [WIDTH - 1:0] fpMultResult;
	wire [WIDTH - 1:0] bitwiseResult;
	assign muxOut = (muxControl ? C : B);
	Multiplier #(.WIDTH(WIDTH)) mult(
		.A(A),
		.B(muxOut),
		.Result(multResult)
	);
	AddSub #(.WIDTH(WIDTH)) addsub(
		.A(A),
		.B(muxOut),
		.AddSub(AddSub),
		.Result(addSubResult)
	);
	fp_addsub fpAddSub(
		.a(A),
		.b(muxOut),
		.subtract(AddSub),
		.y(fpAddResult)
	);
	fp_multiplier fpMult(
		.a(A),
		.b(muxOut),
		.y(fpMultResult)
	);
	BitwiseOperationUnit bitwiseOp(
		.operandA(A),
		.operandB(muxOut),
		.control(bitwiseControl),
		.result(bitwiseResult)
	);
	comparison_unit #(.WIDTH(WIDTH)) compUnit(
		.in1(A),
		.in2(muxOut),
		.control(compControl),
		.predicate(predicate)
	);
	always @(*)
		case (outputControl)
			3'b000: finalResult = addSubResult;
			3'b001: finalResult = fpAddResult;
			3'b010: finalResult = multResult;
			3'b011: finalResult = fpMultResult;
			3'b100: finalResult = bitwiseResult;
			default: finalResult = 0;
		endcase
endmodule
//Moved out into separate file Scalar_Register_File
module Predicate_Register_File (
	clk,
	reset,
	read_addr1,
	read_addr2,
	write_addr1,
	write_addr2,
	write_enable,
	data_out,
	data_in
);
	parameter ADDR_WIDTH = 5;
	parameter DATA_WIDTH = 1;
	parameter NUM_REGISTERS = 32;
	input wire clk;
	input wire reset;
	input wire [ADDR_WIDTH - 1:0] read_addr1;
	input wire [ADDR_WIDTH - 1:0] read_addr2;
	input wire [ADDR_WIDTH - 1:0] write_addr1;
	input wire [ADDR_WIDTH - 1:0] write_addr2;
	input wire write_enable;
	output reg [DATA_WIDTH - 1:0] data_out;
	input wire [DATA_WIDTH - 1:0] data_in;
	reg [DATA_WIDTH - 1:0] register_file [0:NUM_REGISTERS - 1][0:NUM_REGISTERS - 1];
	always @(*) data_out = register_file[read_addr1][read_addr2];
	always @(posedge clk or posedge reset)
		if (reset) begin : sv2v_autoblock_1
			reg signed [31:0] i;
			for (i = 0; i < NUM_REGISTERS; i = i + 1)
				begin : sv2v_autoblock_2
					reg signed [31:0] j;
					for (j = 0; j < NUM_REGISTERS; j = j + 1)
						register_file[i][j] <= 0;
				end
		end
		else if (write_enable)
			register_file[write_addr1][write_addr2] <= data_in;
endmodule
module TopModule (
	clk,
	reset,
	load_recv_msg,
	load_recv_val,
	load_recv_rdy,
	instruction_recv_msg,
	instruction_recv_val,
	instruction_recv_rdy,
	store_send_msg,
	store_send_val,
	store_send_rdy
);
	input wire clk;
	input wire reset;
	input wire [63:0] load_recv_msg;
	input wire load_recv_val;
	output wire load_recv_rdy;
	input wire [31:0] instruction_recv_msg;
	input wire instruction_recv_val;
	output wire instruction_recv_rdy;
	output wire [31:0] store_send_msg;
	output wire store_send_val;
	input wire store_send_rdy;
	wire [63:0] load_send_msg;
	wire load_send_val;
	wire load_send_rdy;
	wire [31:0] instruction_send_msg;
	wire instruction_send_val;
	wire instruction_send_rdy;
	wire [31:0] store_recv_msg;
	wire store_recv_val;
	wire store_recv_rdy;
	wire clock_enable;
	wire clock_bypass;
	wire [4:0] vector_reg_write_select;
	wire [4:0] reg_file_addr1;
	wire [4:0] reg_file_addr2;
	wire mux_bit;
	wire vector_reg_write_bit;
	wire predicate_reg_write_bit;
	wire scalar_reg_write_bit;
	wire vector_reg_load_mux_bit;
	wire scalar_reg_load_mux_bit;
	wire [2:0] functional_unit_mux_bit;
	wire add_subtract_bit;
	wire load_store_bit;
	wire [1:0] bitwise_op_select;
	wire [3:0] predicate_op_select;
	wire [31:0] wb_addr;
	wire [31:0] wb_data;
	wire [31:0] rData1;
	wire [31:0] rData2;
	wire [31:0] functional_unit_output_mux;
	wire [31:0] wData_mux_out;
	wire [4:0] wAddr1_mux_out;
	wire [4:0] wAddr2_mux_out;
	wire [4:0] rAddr1_1_mux_out;
	wire [4:0] rAddr2_1_mux_out;
	wire [4:0] scalar_read_address;
	wire [4:0] scalar_write_address;
	wire [31:0] scalar_write_data;
	wire scalar_write_enable;
	wire [31:0] scalar_read_data;
	wire vector_write_enable;
	wire [31:0] addr_cutoff;
	wire pred_data_out;
	assign vector_write_enable = ((vector_reg_write_bit & !load_store_bit) & pred_data_out) | ((vector_reg_write_bit & load_store_bit) & (wb_addr <= addr_cutoff));
	assign addr_cutoff = 32'h000003ff;
	assign scalar_write_address = (wb_addr[4:0] - addr_cutoff[4:0]) - 1;
	assign scalar_read_address = (load_store_bit ? scalar_write_address : reg_file_addr2);
	assign store_recv_msg = (wb_addr > addr_cutoff ? scalar_read_data : rData1);
	assign store_recv_val = load_store_bit & !vector_reg_write_bit;
	assign load_send_rdy = load_store_bit;
	queue #(
		.WIDTH(64),
		.DEPTH(4)
	) load_queue(
		.clk(clk),
		.reset(reset),
		.recv_msg(load_recv_msg),
		.recv_val(load_recv_val),
		.recv_rdy(load_recv_rdy),
		.send_msg(load_send_msg),
		.send_val(load_send_val),
		.send_rdy(load_send_rdy)
	);
	queue #(
		.WIDTH(32),
		.DEPTH(4)
	) instruction_queue(
		.clk(clk),
		.reset(reset),
		.recv_msg(instruction_recv_msg),
		.recv_val(instruction_recv_val),
		.recv_rdy(instruction_recv_rdy),
		.send_msg(instruction_send_msg),
		.send_val(instruction_send_val),
		.send_rdy(instruction_send_rdy)
	);
	queue #(
		.WIDTH(32),
		.DEPTH(4)
	) store_queue(
		.clk(clk),
		.reset(reset),
		.recv_msg(store_recv_msg),
		.recv_val(store_recv_val),
		.recv_rdy(store_recv_rdy),
		.send_msg(store_send_msg),
		.send_val(store_send_val),
		.send_rdy(store_send_rdy)
	);
	Decoder decoder(
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
	wire [4:0] counter;
	wire done;
	Counter #(
		.WIDTH(5),
		.COUNTER_MAX(31)
	) counter_module(
		.clk(clk),
		.enable(clock_enable),
		.reset(reset),
		.counter(counter),
		.done(done)
	);
	assign instruction_send_rdy = done | clock_bypass;
	assign wb_addr = load_send_msg[63:32];
	assign wb_data = load_send_msg[31:0];
	assign wData_mux_out = (load_store_bit ? wb_data : functional_unit_output_mux);
	assign wAddr1_mux_out = (load_store_bit ? wb_addr[9:5] : vector_reg_write_select);
	assign wAddr2_mux_out = (load_store_bit ? wb_addr[4:0] : counter);
	assign rAddr1_1_mux_out = (load_store_bit ? wb_addr[9:5] : reg_file_addr1);
	assign rAddr2_1_mux_out = (load_store_bit ? wb_addr[4:0] : counter);
VectorRegFile reg_file(
	.clk(clk),
	.reset(reset),
	.rAddr1_1(rAddr1_1_mux_out),
	.rAddr2_1(rAddr2_1_mux_out),
	.rData1(rData1),
	.rAddr1_2(reg_file_addr2),
	.rAddr2_2(counter),
	.rData2(rData2),
	.wAddr1(wAddr1_mux_out),
	.wAddr2(wAddr2_mux_out),
	.wData(wData_mux_out),
	.wEnable(vector_write_enable)
);
	wire pred_data_in;
	ALU #(.WIDTH(32)) alu(
		.A(rData1),
		.B(rData2),
		.C(scalar_read_data),
		.AddSub(add_subtract_bit),
		.muxControl(mux_bit),
		.outputControl(functional_unit_mux_bit),
		.bitwiseControl(bitwise_op_select),
		.compControl(predicate_op_select),
		.finalResult(functional_unit_output_mux),
		.predicate(pred_data_in)
	);
	assign scalar_write_data = wb_data;
	assign scalar_write_enable = (load_store_bit & vector_reg_write_bit) & (wb_addr > addr_cutoff);
Scalar_Register_File scalar_reg_file(
	.clk(clk),
	.reset(reset),
	.read_address(scalar_read_address),
	.write_address(scalar_write_address),
	.write_data(scalar_write_data),
	.write_enable(scalar_write_enable),
	.read_data(scalar_read_data)
);

	wire [4:0] pred_read_addr1;
	wire [4:0] pred_read_addr2;
	wire [4:0] pred_write_addr1;
	wire [4:0] pred_write_addr2;
	wire pred_write_enable;
	assign pred_read_addr1 = vector_reg_write_select;
	assign pred_read_addr2 = counter;
	assign pred_write_addr1 = vector_reg_write_select;
	assign pred_write_addr2 = counter;
	assign pred_write_enable = predicate_reg_write_bit;
	Predicate_Register_File #(
		.ADDR_WIDTH(5),
		.DATA_WIDTH(1),
		.NUM_REGISTERS(32)
	) predicate_reg_file(
		.clk(clk),
		.reset(reset),
		.read_addr1(pred_read_addr1),
		.read_addr2(pred_read_addr2),
		.write_addr1(pred_write_addr1),
		.write_addr2(pred_write_addr2),
		.write_enable(pred_write_enable),
		.data_out(pred_data_out),
		.data_in(pred_data_in)
	);
endmodule
module WrapperBlock (
	wb_clk_i,
	wb_rst_i,
	wbs_stb_i,
	wbs_cyc_i,
	wbs_we_i,
	wbs_sel_i,
	wbs_dat_i,
	wbs_adr_i,
	wbs_ack_o,
	wbs_dat_o,
	clk,
	reset
);
	input wb_clk_i;
	input wb_rst_i;
	input wbs_stb_i;
	input wbs_cyc_i;
	input wbs_we_i;
	input [3:0] wbs_sel_i;
	input [31:0] wbs_dat_i;
	input [31:0] wbs_adr_i;
	output wire wbs_ack_o;
	output wire [31:0] wbs_dat_o;
	input wire clk;
	input wire reset;
	wire [63:0] load_recv_msg_internal;
	wire load_recv_val_internal;
	wire load_recv_rdy_internal;
	wire [31:0] instruction_recv_msg_internal;
	wire instruction_recv_val_internal;
	wire instruction_recv_rdy_internal;
	wire [31:0] store_send_msg_internal;
	wire store_send_val_internal;
	wire store_send_rdy_internal;
	wb_converter wb_converter_inst(
		.wb_clk_i(clk),
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
	TopModule TopModule_inst(
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
module WrapperBlock_noparam (
	`ifdef USE_POWER_PINS
    inout wire vccd1,	// User area 1 1.8V supply
    inout wire vssd1,	// User area 1 digital ground
	`endif
	input wire [0:0] clk,
	input wire [0:0] reset,
	input wire [0:0] wb_clk_i,
	input wire [0:0] wb_rst_i,
	output wire [0:0] wbs_ack_o,
	input wire [31:0] wbs_adr_i,
	input wire [0:0] wbs_cyc_i,
	input wire [31:0] wbs_dat_i,
	output wire [31:0] wbs_dat_o,
	input wire [3:0] wbs_sel_i,
	input wire [0:0] wbs_stb_i,
	input wire [0:0] wbs_we_i
);
	WrapperBlock v(
		.clk(clk),
		.reset(reset),
		.wb_clk_i(wb_clk_i),
		.wb_rst_i(wb_rst_i),
		.wbs_ack_o(wbs_ack_o),
		.wbs_adr_i(wbs_adr_i),
		.wbs_cyc_i(wbs_cyc_i),
		.wbs_dat_i(wbs_dat_i),
		.wbs_dat_o(wbs_dat_o),
		.wbs_sel_i(wbs_sel_i),
		.wbs_stb_i(wbs_stb_i),
		.wbs_we_i(wbs_we_i)
	);
endmodule

