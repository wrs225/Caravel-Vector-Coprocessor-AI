module fp_multiplier(
    input logic [31:0] a, // input a
    input logic [31:0] b, // input b
    output logic [31:0] y // output y
);
    logic [7:0] a_exponent, b_exponent, y_exponent_temp, y_exponent;
    logic [23:0] a_mantissa, b_mantissa;
    logic [47:0] mult_result;
    logic [22:0] y_mantissa_temp, y_mantissa;
    logic a_sign, b_sign, y_sign;
    logic sticky_bit;

    // Extract the sign, exponent, and mantissa from the inputs
    assign a_sign = a[31];
    assign a_exponent = a[30:23];
    assign a_mantissa = {1'b1, a[22:0]};

    assign b_sign = b[31];
    assign b_exponent = b[30:23];
    assign b_mantissa = {1'b1, b[22:0]};

    // Perform the multiplication
    assign y_sign = a_sign ^ b_sign;
    assign mult_result = a_mantissa * b_mantissa;
    assign y_exponent_temp = a_exponent + b_exponent - 127 + mult_result[47];
    assign y_mantissa_temp = mult_result[47] ? mult_result[46:24] : mult_result[45:23];
    assign sticky_bit = mult_result[47] ? |mult_result[22:0] : |mult_result[21:0];

    // Check for infinities and NaNs
    always_comb begin
        if ((a == 32'b0 && b_exponent == 8'hFF && b_mantissa[22:0] == 0) || (b == 32'b0 && a_exponent == 8'hFF && a_mantissa[22:0] == 0)) begin
            // a is zero and b is infinity, or b is zero and a is infinity, result is NaN
            y_exponent = 8'hFF;
            y_mantissa = 23'h400000; // Set mantissa to 23'h400000 for NaN cases
        end else if (a == 32'b0 || b == 32'b0) begin
            // If either input is zero, output is zero
            y_exponent = 8'h00;
            y_mantissa = 23'h0;
        end else if (a_exponent == 8'hFF || b_exponent == 8'hFF) begin
            // a or b is NaN, result is NaN
            y_exponent = 8'hFF;
            y_mantissa = 23'h400000; // Set mantissa to 23'h400000 for NaN cases
        end else begin
            // Normal case
            y_exponent = y_exponent_temp;
            y_mantissa = y_mantissa_temp;
        end
    end

    // Combine the sign, exponent, and mantissa into the output
    assign y = {y_sign, y_exponent, y_mantissa};
endmodule


/* Add a bit called r. If the highest order bit of mult_result is one, then r becomes the value of mult_result[23], otherwise r is [22]*/