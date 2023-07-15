module Multiplier #(parameter WIDTH = 32) (
    input logic [WIDTH-1:0] A,
    input logic [WIDTH-1:0] B,
    output logic [WIDTH-1:0] Result
);
    always_comb begin
        Result = A * B;
    end
endmodule