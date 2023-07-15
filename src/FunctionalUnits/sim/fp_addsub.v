module fp_addsub #(parameter WIDTH = 32)
(
    input logic [WIDTH-1:0] a, b,
    input logic subtract,
    output logic [WIDTH-1:0] y
);

    // Extract fields
    logic [WIDTH-2:WIDTH-9] a_exp, b_exp;
    logic [WIDTH-10:0] a_mant, b_mant;
    logic a_sign, b_sign;
    assign a_sign = a[WIDTH-1];
    assign a_exp = a[WIDTH-2:WIDTH-9];
    assign a_mant = {1'b1, a[WIDTH-10:0]};
    assign b_sign = b[WIDTH-1];
    assign b_exp = b[WIDTH-2:WIDTH-9];
    assign b_mant = {1'b1, b[WIDTH-10:0]};

    // Align mantissas
    logic [WIDTH-1:0] a_mant_align, b_mant_align;
    logic [WIDTH-2:WIDTH-9] exp_diff;
    assign exp_diff = a_exp - b_exp;
    assign a_mant_align = a_mant << exp_diff;
    assign b_mant_align = b_mant;

    // Perform addition or subtraction
    logic [WIDTH-1:0] sum;
    assign sum = subtract ? a_mant_align - b_mant_align : a_mant_align + b_mant_align;

    // Normalize result
    logic [WIDTH-2:WIDTH-9] y_exp;
    logic [WIDTH-10:0] y_mant;
    assign y_exp = a_exp + ($clog2(sum[WIDTH-1:WIDTH-10]) - WIDTH + 10);
    assign y_mant = sum[WIDTH-10:0];

    // Handle overflow and underflow
    assign y_exp = (y_exp > 255) ? 255 : (y_exp < 0) ? 0 : y_exp;
    assign y_mant = (y_exp == 255 || y_exp == 0) ? 0 : y_mant;

    // Handle NaN and infinity
    assign y = (a_exp == 255 && a_mant != 0) || (b_exp == 255 && b_mant != 0) ? {1'b1, 8'b11111111, 23'b1} :
               (a_exp == 255 && a_mant == 0 && a_sign != subtract) || (b_exp == 255 && b_mant == 0 && b_sign == subtract) ? {1'b0, 8'b11111111, 23'b0} :
               {a_sign ^ subtract, y_exp, y_mant[WIDTH-11:0]};

endmodule