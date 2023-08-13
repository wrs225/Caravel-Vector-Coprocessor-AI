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
    logic full, empty, next_full, next_empty;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            head <= 0;
            tail <= 0;
            full <= 0;
            empty <= 1;
        end else begin
            head <= (send_rdy && send_val && !empty) ? (head == DEPTH-1 ? 0 : head + 1) : head;
            tail <= (recv_rdy && recv_val && !full) ? (tail == DEPTH-1 ? 0 : tail + 1) : tail;
            full <= next_full;
            empty <= next_empty;
        end
    end

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            // Resetting the contents of the queue
            for (int i = 0; i < DEPTH; i++) begin
                queue[i] <= '0;
            end
        end else if (recv_rdy && recv_val && !full) begin
            queue[tail] <= recv_msg;
        end
    end

    always_comb begin
        next_full = full;
        next_empty = empty;

        if (recv_rdy && recv_val && !full) begin
            if (send_rdy && send_val && !empty) begin
                // If sending and receiving simultaneously, the full and empty state remain the same
            end else begin
                next_full = (tail == (DEPTH-1) ? 0 : tail + 1) == head;
                next_empty = 0;
            end
        end else if (send_rdy && send_val && !empty) begin
            next_empty = (head == (DEPTH-1) ? 0 : head + 1) == tail;
            next_full = 0;
        end
    end

    assign recv_rdy = !full;
    assign send_val = !empty;
    assign send_msg = queue[head];

endmodule
