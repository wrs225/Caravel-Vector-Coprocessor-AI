module BitwiseOperationUnit(
    input [31:0] operandA, // first input
    input [31:0] operandB, // second input
    input [1:0] control, // control signals
    output [31:0] result // result
);

    reg [31:0] result_reg; // Define the 'result' as 'reg' type

    always_comb begin
        case(control)
            2'b00: result_reg = operandA & operandB; // AND operation
            2'b01: result_reg = operandA | operandB; // OR operation
            2'b10: result_reg = operandA ^ operandB; // XOR operation
            default: result_reg = 32'b0; // Default case, result is zero
        endcase
    end

    assign result = result_reg; // Assign the 'result_reg' to 'result'

endmodule
