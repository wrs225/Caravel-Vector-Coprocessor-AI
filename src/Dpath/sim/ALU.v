`include "../FunctionalUnits/sim/Multiplier.v"
`include "../FunctionalUnits/sim/AddSub.v"
`include "../FunctionalUnits/sim/fp_addsub.v"
`include "../FunctionalUnits/sim/fp_multiplier.v"
`include "../FunctionalUnits/sim/BitwiseOperationUnit.v"
`include "../FunctionalUnits/sim/comparison_unit.v"

module ALU #(parameter WIDTH = 32) (
    input logic [WIDTH-1:0] A,
    input logic [WIDTH-1:0] B,
    input logic [WIDTH-1:0] C,
    input logic AddSub, // 0 for Add, 1 for Subtract
    input logic muxControl, // 0 for B, 1 for C
    input logic [2:0] outputControl, // Output mux control
    input logic [1:0] bitwiseControl, // Control for BitwiseOperationUnit
    input logic [1:0] compControl, // Control for comparison_unit
    output logic [WIDTH-1:0] finalResult, // Muxed output
    output logic predicate
);

    logic [WIDTH-1:0] muxOut;
    logic [WIDTH-1:0] multResult;
    logic [WIDTH-1:0] addSubResult;
    logic [WIDTH-1:0] fpAddResult;
    logic [WIDTH-1:0] fpMultResult;
    logic [WIDTH-1:0] bitwiseResult;

    // Multiplexer for inputs
    assign muxOut = muxControl ? C : B;

    // Instantiate Multiplier
    Multiplier #(WIDTH) mult (
        .A(A),
        .B(muxOut),
        .Result(multResult)
    );

    // Instantiate AddSub
    AddSub #(WIDTH) addsub (
        .A(A),
        .B(muxOut),
        .AddSub(AddSub),
        .Result(addSubResult)
    );

    // Instantiate fp_addsub
    fp_addsub fpAddSub (
        .a(A),
        .b(muxOut),
        .subtract(AddSub),
        .y(fpAddResult)
    );

    // Instantiate fp_multiplier
    fp_multiplier fpMult (
        .a(A),
        .b(muxOut),
        .y(fpMultResult)
    );

    // Instantiate BitwiseOperationUnit
    BitwiseOperationUnit bitwiseOp (
        .operandA(A),
        .operandB(muxOut),
        .control(bitwiseControl),
        .result(bitwiseResult)
    );

    // Instantiate comparison_unit
    comparison_unit #(WIDTH) compUnit (
        .in1(A),
        .in2(muxOut),
        .control(compControl),
        .predicate(predicate)
    );

    // Multiplexer for outputs
    always_comb begin
        case (outputControl)
            3'b000: finalResult = addSubResult;
            3'b001: finalResult = fpAddResult;
            3'b010: finalResult = multResult;
            3'b011: finalResult = fpMultResult;
            3'b100: finalResult = bitwiseResult;
            default: finalResult = 0;
        endcase
    end
endmodule
