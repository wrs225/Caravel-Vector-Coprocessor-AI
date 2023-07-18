module comparison_unit #(parameter WIDTH = 32)(
    input logic [WIDTH-1:0] in1,
    input logic [WIDTH-1:0] in2,
    input logic [1:0] control,
    output logic predicate
);

    always_comb begin
        case(control)
            2'b00: predicate = (in1 == in2); // Set if equal
            2'b01: predicate = (in1 != in2); // Set if not equal
            2'b10: predicate = (in1 > in2);  // Set if greater than
            2'b11: predicate = (in1 < in2);  // Set if less than
            default: predicate = 0;
        endcase
    end

endmodule