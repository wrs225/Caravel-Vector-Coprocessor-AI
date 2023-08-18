module fp_addsub (
    input logic [31:0] a,
    input logic [31:0] b,
    input logic subtract,
    output logic [31:0] y
);

    logic [31:0] b_neg;
    logic a_sign, b_sign;
    logic [7:0] a_exp, b_exp;
    logic [23:0] a_frac, b_frac;  // Increase fraction size to 24 bits
    logic y_sign;
    logic [7:0] y_exp;
    logic [23:0] y_frac;  // Increase fraction size to 24 bits
    logic [47:0] y_frac_intermediate;  // Intermediate fraction for normalization extended to 48 bits
    logic [7:0] y_exp_intermediate;  // Intermediate exponent for normalization
    logic [5:0] shift_amount;  // Shift amount from priority encoder

    // Negate b if subtract is high
    assign b_neg = subtract ? {b[31]^1'b1, b[30:0]} : b;

    // Priority encoder to find the leading one
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

    // Add or subtract
    always_comb begin
        // Extract fields
        a_sign     = a[31];
        b_sign     = b_neg[31];
        a_exp = a[30:23];
        b_exp = b_neg[30:23];
        a_frac = {1'b1, a[22:0]};  // Add implicit leading 1
        b_frac = {1'b1, b_neg[22:0]};  // Add implicit leading 1

        // Perform addition or subtraction
        if (a_exp > b_exp) begin
            y_exp_intermediate = a_exp;
            if (b_sign ^ a_sign) begin
                y_frac_intermediate = a_frac - (b_frac >> (a_exp - b_exp));  // Corrected shift amount
            end else begin
                y_frac_intermediate = a_frac + (b_frac >> (a_exp - b_exp));  // Corrected shift amount
            end
            y_sign = a_sign;
        end else if (a_exp < b_exp) begin
            y_exp_intermediate = b_exp;
            if (b_sign ^ a_sign) begin
                y_frac_intermediate = b_frac - (a_frac >> (b_exp - a_exp));  // Corrected shift amount
            end else begin
                y_frac_intermediate = (a_frac >> (b_exp - a_exp)) + b_frac;  // Corrected shift amount
            end
            y_sign = b_sign;
        end else begin
            y_exp_intermediate = a_exp;
            if (a_frac >= b_frac) begin
                if (b_sign ^ a_sign) begin
                    y_frac_intermediate = a_frac - b_frac;  // No shift when exponents are equal
                end else begin
                    y_frac_intermediate = a_frac + b_frac;  // No shift when exponents are equal
                end
                y_sign = a_sign;
            end else begin
                if (b_sign ^ a_sign) begin
                    y_frac_intermediate = b_frac - a_frac;  // No shift when exponents are equal
                end else begin
                    y_frac_intermediate = b_frac + a_frac;  // No shift when exponents are equal
                end
                y_sign = b_sign;
            end
        end

        // Normalize result using priority encoder
        if (a == 32'b0 && b == 32'b0) begin
            shift_amount = 6'b000000;  // No shift if both inputs are zero
        end else begin
            shift_amount = y_frac_intermediate[47] ? 6'b000000 : priority_encoder(y_frac_intermediate);
        end

        // Shift fraction and adjust exponent
        if (shift_amount[5]) begin  // If the most significant bit is 1, shift_amount is negative
            y_frac = y_frac_intermediate >> -shift_amount;  // Right shift
        end else begin
            y_frac = y_frac_intermediate << shift_amount;  // Left shift
        end
        y_exp = y_exp_intermediate - {{2{shift_amount[5]}}, shift_amount};  // Sign extend shift_amount and subtract from y_exp_intermediate

    end

    // Check for infinity and pack fields into output
    always_comb begin
        // Check if either input is infinity
        if ((a[30:23] == 8'hFF && a[22:0] == 23'b0) && (b_neg[30:23] == 8'hFF && b_neg[22:0] == 23'b0)) begin
            // If both inputs are infinity and the operation is subtraction, the output is NaN
            if (subtract && (a_sign ^ b_sign)) begin
                y = {1'b0, 8'hFF, 23'h400000};
            end else if (a_sign ^ b_sign) begin
                y = {a_sign, 8'hFF, 23'b0};
            end else begin
                y = {y_sign, y_exp, y_frac[22:0]};  // Only take the lower 23 bits of the fraction
            end
        end else if ((a[30:23] == 8'hFF && a[22:0] == 23'b0) || (b_neg[30:23] == 8'hFF && b_neg[22:0] == 23'b0)) begin
            // If either input is infinity (but not both), set the output to infinity as well
            y = {a_sign | b_sign, 8'hFF, 23'b0};
        end else if (y_frac_intermediate == 48'b0) begin
            y = 32'b0;
        end else begin
            // If neither input is infinity and the output is not zero, perform regular assignment
            y = {y_sign, y_exp, y_frac[22:0]};  // Only take the lower 23 bits of the fraction
        end
    end
endmodule
