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
    logic full, empty;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            head <= 0;
            tail <= 0;
            full <= 0;
            empty <= 1;
        end else begin
            // Temporarily store the next values
            logic next_full, next_empty;
            logic [$clog2(DEPTH)-1:0] next_head, next_tail;

            next_head = head;
            next_tail = tail;
            next_full = full;
            next_empty = empty;

            // Receive logic
            if (recv_rdy && recv_val && !full) begin
                queue[tail] = recv_msg;
                next_tail = tail + 1;
                if (next_tail == DEPTH) next_tail = 0;
                if (next_tail == head) next_full = 1;
                next_empty = 0;
            end

            // Send logic
            if (send_rdy && send_val && !empty) begin
                next_head = head + 1;
                if (next_head == DEPTH) next_head = 0;
                if (next_head == tail) next_empty = 1;
                next_full = 0;
            end

            // Update values
            head <= next_head;
            tail <= next_tail;
            full <= next_full;
            empty <= next_empty;
        end
    end

    assign recv_rdy = !full;
    assign send_val = !empty;
    assign send_msg = queue[head];

endmodule
