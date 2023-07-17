module BitwiseOperationUnit(
    input [31:0] operandA, // first input
    input [31:0] operandB, // second input
    input [1:0] control, // control signals
    output [31:0] result // result
);

    always_comb begin
        case(control)
            2'b00: result = operandA & operandB; // AND operation
            2'b01: result = operandA | operandB; // OR operation
            2'b10: result = operandA ^ operandB; // XOR operation
            default: result = 32'b0; // Default case, result is zero
        endcase
    end

endmodule