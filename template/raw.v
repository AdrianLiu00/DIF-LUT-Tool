module $$FUNC$$_diflut (
    data_in,
    data_out,
    
    clk,
    rsn
);

//-------------------------------------------------------
// Parameters

localparam INPUT_BIT = $$INPUT_BIT$$;
localparam OUTPUT_BIT = $$OUTPUT_BIT$$;
localparam KEY_BIT = $$KEY_BIT$$;
localparam WORD_BIT = $$WORD_BIT$$;


//-------------------------------------------------------
// Declaration

input signed [INPUT_BIT-1:0] data_in;
output signed reg [OUTPUT_BIT-1:0] data_out;

input clk;
input rsn;

wire [WORD_BIT-1:0] pwl_val;

wire [WORD_BIT-1:0] lut_val;
wire [WORD_BIT-1:0] lut_val_pos;
wire [WORD_BIT-1:0] lut_val_neg;

wire [WORD_BIT-1:0] out_pos;


//-------------------------------------------------------
// Input

reg [KEY_BIT-1:0] in_reg;
always @(posedge clk or negedge rsn) begin
    if (!rsn)
        in_reg <= {KEY_BIT{1'b0}};
    else
        in_reg <= data_in[INPUT_BIT-1 -: KEY_BIT];
end


//-------------------------------------------------------
// Piecewise linear matching

always @(*) begin
$$PWL_HDL$$
end

//-------------------------------------------------------
// Range addressable look-up table

// (* DONT_TOUCH = "yes" *)
dif_lut_K$$KEY_BIT$$W$$WORD_BIT$$ lut0(
    .key(in_reg[KEY_BIT-1:0]),
    .value(lut_val_pos)
);

// (* DONT_TOUCH = "yes" *) 
dif_lut_K$$KEY_BIT$$W$$WORD_BIT$$_sym lut1(
    .key(in_reg[KEY_BIT-1:0]),
    .value(lut_val_neg)
);

assign lut_val = {in_reg[KEY_BIT-1]? lut_val_neg:lut_val_pos};


//-------------------------------------------------------
// Add and Output

// adder ip
add_data add_u0(
    .A      (pwl_val),
    .B      (lut_val),
    .S      (out_pos)
);

always @(posedge clk) begin
    if(!rsn)
        data_out <= {OUTPUT_BIT{1'b0}};
    else
        data_out <= {out_pos, {(OUTPUT_BIT-WORD_BIT){1'b0}}};
end

endmodule