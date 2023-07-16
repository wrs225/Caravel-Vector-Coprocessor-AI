module fp_multiplier(
    input logic [31:0] a, // input a
    input logic [31:0] b, // input b
    output logic [31:0] y // output y
);

    logic [7:0] a_exp, b_exp, y_exp;
    logic [22:0] a_mant, b_mant, y_mant;
    logic a_sign, b_sign, y_sign;
    logic [47:0] mult_result;
    logic overflow, underflow;

    // Extract sign, exponent, and mantissa
    assign a_sign = a[31];
    assign a_exp = a[30:23];
    assign a_mant = a[22:0];

    assign b_sign = b[31];
    assign b_exp = b[30:23];
    assign b_mant = b[22:0];

    // Multiply mantissas
    assign mult_result = (a_mant | 24'b1 << 23) * (b_mant | 24'b1 << 23);

    // Normalize result
    always_comb begin
        if (mult_result[47]) begin
            y_mant = mult_result[46:24];
            overflow = 1'b1;
        end else begin
            y_mant = mult_result[45:23];
            overflow = 1'b0;
        end
    end

    // Add exponents
    assign y_exp = a_exp + b_exp - 127;

    // Determine sign of result
    assign y_sign = a_sign ^ b_sign;

    // Check for overflow and underflow
    always_comb begin
        if (y_exp[7]) begin
            y_exp = 255;
            y_mant = 0;
            if (overflow) begin
                y_sign = 1'b1;
            end
        end else if (!y_exp) begin
            y_exp = 0;
            y_mant = 0;
            y_sign = 1'b0;
        end
    end

    // Check for NaN and Inf
    always_comb begin
        if (a_exp == 255 && a_mant != 0 || b_exp == 255 && b_mant != 0) begin
            // NaN
            y_exp = 255;
            y_mant = 1;
        end else if (a_exp == 255 && a_mant == 0 || b_exp == 255 && b_mant == 0) begin
            // Inf
            y_exp = 255;
            y_mant = 0;
        end
    end

    // Combine sign, exponent, and mantissa into final result
    assign y = {y_sign, y_exp, y_mant};

endmodule