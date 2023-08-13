module Decoder (
    input logic [31:0] instruction,
    input logic instruction_valid,
    output logic [4:0] reg_file_addr1,
    output logic [4:0] reg_file_addr2,
    output logic mux_bit,
    output logic vector_reg_write_bit,
    output logic predicate_reg_write_bit,
    output logic scalar_reg_write_bit,
    output logic vector_reg_load_mux_bit,
    output logic scalar_reg_load_mux_bit,
    output logic [2:0] functional_unit_mux_bit,
    output logic add_subtract_bit,
    output logic load_store_bit,
    output logic clock_enable,
    output logic clock_bypass,
    output logic [1:0] bitwise_op_select,
    output logic [3:0] predicate_op_select,
    output logic [4:0] vector_reg_write_select
);

logic [4:0] opcode;

always_comb begin
    if (instruction_valid == 1'b0) begin
        reg_file_addr1 = 5'b0;
        reg_file_addr2 = 5'b0;
        mux_bit = 1'b0;
        vector_reg_write_bit = 1'b0;
        predicate_reg_write_bit = 1'b0;
        scalar_reg_write_bit = 1'b0;
        vector_reg_load_mux_bit = 1'b0;
        scalar_reg_load_mux_bit = 1'b0;
        functional_unit_mux_bit = 3'b0;
        add_subtract_bit = 1'b0;
        load_store_bit = 1'b0;
        clock_enable = 1'b0;
        clock_bypass = 1'b1;
        bitwise_op_select = 2'b0;
        predicate_op_select = 4'b0;
        vector_reg_write_select = 5'b0;
    end else begin
        reg_file_addr1 = instruction[20:16];
        reg_file_addr2 = instruction[15:11];
        vector_reg_write_select = instruction[25:21];
        opcode = instruction[31:27];
        case(opcode)
            5'b00000, 5'b00001: begin // Load/Store instructions (VLOAD, VSTORE)
                clock_bypass = 1;
                clock_enable = 0;
                mux_bit = 0;
                vector_reg_write_bit = (opcode == 5'b00000) ? 1 : 0;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 0;
                add_subtract_bit = 0;
                load_store_bit = 1;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b00;
            end
            5'b00010, 5'b00011, 5'b00110: begin // Vector/Scalar add/sub instructions (VADD, VSUB, VSADD)
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = (opcode == 5'b00110) ? 1 : 0;
                vector_reg_write_bit = 1;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 0;
                add_subtract_bit = (opcode == 5'b00011) ? 1 : 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b00;
            end
            5'b00100, 5'b00101: begin // Vector/Scalar mul instructions (VMUL, VSMUL)
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = (opcode == 5'b00101) ? 1 : 0;
                vector_reg_write_bit = 1;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 2;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b00;
            end
            5'b00111, 5'b10000: begin // Floating point add/sub instructions (VFADD, VFSUB)
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 1;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 1;
                add_subtract_bit = (opcode == 5'b10000) ? 1 : 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b00;
            end
            5'b01000: begin // Floating point multiplication (VFMUL)
                clock_enable = 1;
                vector_reg_write_bit = 1;
                functional_unit_mux_bit = 3'b011;
                mux_bit = 0;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                add_subtract_bit = 0;
                load_store_bit = 0;
                clock_bypass = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b00;
            end
            5'b01001, 5'b01010, 5'b01011: begin // Bitwise instructions (VAND, VOR, VXOR)
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 1;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 4;
                add_subtract_bit = 0;
                load_store_bit = 0;
                if (opcode == 5'b01001) begin
                    bitwise_op_select = 2'b00; // VAND
                end else if (opcode == 5'b01010) begin
                    bitwise_op_select = 2'b01; // VOR
                end else if (opcode == 5'b01011) begin
                    bitwise_op_select = 2'b10; // VXOR
                end
                predicate_op_select = 4'b00;
            end
            5'b01100: begin // VPSETZ
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0000;
            end
            5'b01101: begin // VPSETN
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0001;
            end
            5'b01110: begin // VPSET
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0010;
            end
            5'b01111: begin // VPSGE
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0011;
            end
            5'b11000: begin // VPSLT
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0100;
            end
            5'b10001: begin // VPUGE
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0101;
            end
            5'b10010: begin // VPULT
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0110;
            end
            5'b10100: begin // VPEQ
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b0111;
            end
            5'b10111: begin // VPNEQ
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 0;
                vector_reg_write_bit = 0;
                predicate_reg_write_bit = 1;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 5;
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b1000;
            end
            5'b10101: begin // VFSMUL instruction (0x15)
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 1; // Using a scalar value
                vector_reg_write_bit = 1;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 3'b011; // Select multiplication
                add_subtract_bit = 0;
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b00;
            end
            
            5'b10110: begin // VFSADD instruction (0x16)
                clock_bypass = 0;
                clock_enable = 1;
                mux_bit = 1; // Using a scalar value
                vector_reg_write_bit = 1;
                predicate_reg_write_bit = 0;
                scalar_reg_write_bit = 0;
                vector_reg_load_mux_bit = 0;
                scalar_reg_load_mux_bit = 0;
                functional_unit_mux_bit = 1; // Select addition
                add_subtract_bit = 0; // Select addition
                load_store_bit = 0;
                bitwise_op_select = 2'b00;
                predicate_op_select = 4'b00;
            end

            default: begin // Unrecognized opcode
                reg_file_addr1 = 5'b0;
                reg_file_addr2 = 5'b0;
                mux_bit = 1'b0;
                vector_reg_write_bit = 1'b0;
                predicate_reg_write_bit = 1'b0;
                scalar_reg_write_bit = 1'b0;
                vector_reg_load_mux_bit = 1'b0;
                scalar_reg_load_mux_bit = 1'b0;
                functional_unit_mux_bit = 3'b0;
                add_subtract_bit = 1'b0;
                load_store_bit = 1'b0;
                clock_enable = 1'b0;
                clock_bypass = 1'b1;
                bitwise_op_select = 2'b0;
                predicate_op_select = 4'b0;
                vector_reg_write_select = 5'b0;
            end
        endcase
    end
end

endmodule
