`timescale 1ns/1ns

module  $$FUNC$$_measure_tb();

//-------------------------------------------------------
// Parameters

localparam INPUT_BIT = $$INPUT_BIT$$;
localparam OUTPUT_BIT = $$OUTPUT_BIT$$;

reg     clk,rsn;
reg [INPUT_BIT-1:0]   data_in;
wire [OUTPUT_BIT-1:0]  data_out;

$$FUNC$$_diflut $$FUNC$$_diflut_u0(
    .data_in        (data_in),
    .data_out       (data_out),
    .clk            (clk),
    .rsn            (rsn)
);

integer     file;
initial begin
   file = $fopen($$OUTPUT_FILE$$,"w");  
end


reg [INPUT_BIT:0]   seed;

initial forever #5 clk = ~clk;

initial begin
    $display("*********** START ************");
    clk = 1'b0;
    rsn = 1'b0;

    #10
    rsn = 1'b1;

    #10
    for(seed = 'b0; seed < {1'b1, $$INPUT_BIT$$'b0}; seed = seed + 'b1) begin
        #10
        data_in <= seed[INPUT_BIT-1:0];

        #20
        $fdisplay(file, "in=%b", data_in);
        $fdisplay(file, "out=%b\n", data_out);
        if (seed%200 == 0) begin
            $display("Processing: %d / $$INPUT_NUM$$ --- %2.2f%%", seed, 100*seed/$$INPUT_NUM$$);
        end
    end


    $display("*********** DONE ************");
    $fclose(file);
    $finish;
end


endmodule