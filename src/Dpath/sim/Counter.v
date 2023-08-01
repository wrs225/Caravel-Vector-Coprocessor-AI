module Counter #(parameter WIDTH = 4, COUNTER_MAX = 2**WIDTH-1) (
    input logic clk,
    input logic enable,
    input logic reset,
    output logic [WIDTH-1:0] counter,
    output logic done
);

    always_ff @(posedge clk or posedge reset) begin
        if (reset)
            counter <= 0;  // Reset the counter when reset signal goes high
        else if (enable)
            counter <= counter + 1;  // Increment the counter if enable is high
    end

    // Check if the counter has reached the maximum value
    assign done = (counter == COUNTER_MAX) ? 1'b1 : 1'b0;

endmodule