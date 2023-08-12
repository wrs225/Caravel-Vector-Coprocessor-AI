module comparison_unit #(parameter WIDTH = 32)(
    input logic [WIDTH-1:0] in1,
    input logic [WIDTH-1:0] in2,
    input logic [3:0] control,
    output logic predicate
);

always_comb begin
    case (control)
        4'b0000: predicate = (in1 == 0); // VPSETZ
        4'b0001: predicate = (in1 != 0); // VPSETN
        4'b0010: predicate = 1;           // VPSET
        4'b0011: predicate = ($signed(in1) >= $signed(in2)); // VPSGE, signed comparison
        4'b0100: predicate = ($signed(in1) < $signed(in2));  // VPSLT, signed comparison
        4'b0101: predicate = (in1 >= in2); // VPUGE, treating inputs as unsigned
        4'b0110: predicate = (in1 < in2);  // VPULT, treating inputs as unsigned
        4'b0111: predicate = (in1 == in2); // VPEQ
        4'b1000: predicate = (in1 != in2); // VPNEQ
        default: predicate = 0;            // Default case
    endcase
end

endmodule
