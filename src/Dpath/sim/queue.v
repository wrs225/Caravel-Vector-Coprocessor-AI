module queue #(parameter WIDTH = 8, DEPTH = 16) (
    input logic clk,
    input logic reset,

    // Receive interface
    input logic [WIDTH-1:0] recv_msg,
    input logic recv_val,
    output logic recv_rdy,

    // Send interface
    output logic [WIDTH-1:0] send_msg,
    output logic send_val,
    input logic send_rdy
);

    typedef logic [WIDTH-1:0] data_t;
    data_t queue [0:DEPTH-1];
    logic [$clog2(DEPTH)-1:0] head, tail;
    logic [$clog2(DEPTH)-1:0] count;
    logic full, empty;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            head <= 0;
            tail <= 0;
            count <= 0;
            full <= 0;
            empty <= 1;
        end else begin
            if (recv_rdy && recv_val && !full) begin
                queue[tail] <= recv_msg;
                tail <= tail + 1;
                if (tail == DEPTH)
                    tail <= 0;
                count <= count + 1;
            end
            if (send_rdy && send_val && !empty) begin
                head <= head + 1;
                if (head == DEPTH)
                    head <= 0;
                count <= count - 1;
            end
            full <= (count == DEPTH);
            empty <= (count == 0);
        end
    end

    assign recv_rdy = !full;
    assign send_val = !empty;
    assign send_msg = queue[head];

endmodule
