module AddSub #(parameter WIDTH = 32) (
    input logic [WIDTH-1:0] A,
    input logic [WIDTH-1:0] B,
    input logic AddSub, // 0 for Add, 1 for Subtract
    output logic [WIDTH-1:0] Result
);
    always_comb begin
        if (AddSub == 0) begin
            Result = A + B;
        end else begin
            Result = A - B;
        end
    end
endmodule