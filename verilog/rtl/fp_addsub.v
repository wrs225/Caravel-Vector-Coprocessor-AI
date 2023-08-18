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
    priority_encoder = 6'b000000; // Default value
    for (i = 47; i >= 0; i = i - 1) begin
        if (in[i]) begin
            priority_encoder = 23 - i;
            i = -1; // Break the loop by setting i to an invalid value
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