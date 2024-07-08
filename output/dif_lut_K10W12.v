// @ KEY_BIT=10	 WORD_BIT=12
module dif_lut_K10W12 (
    input signed [9:0]     key,
    output signed [11:0]    value
);

wire [18 : 0] comp;
reg  [11 : 0] value;

assign comp[0] = key < 10'b0000110000;
assign comp[1] = key < 10'b0001000100;
assign comp[2] = key < 10'b0001010011;
assign comp[3] = key < 10'b0001100000;
assign comp[4] = key < 10'b0001101011;
assign comp[5] = key < 10'b0001110101;
assign comp[6] = key < 10'b0001111111;
assign comp[7] = key < 10'b0010001000;
assign comp[8] = key < 10'b0010010001;
assign comp[9] = key < 10'b0010011011;
assign comp[10] = key < 10'b0010100110;
assign comp[11] = key < 10'b0010110010;
assign comp[12] = key < 10'b0010111111;
assign comp[13] = key < 10'b0011001110;
assign comp[14] = key < 10'b0011100000;
assign comp[15] = key < 10'b0011110110;
assign comp[16] = key < 10'b0100010101;
assign comp[17] = key < 10'b0101100000;
assign comp[18] = key < 10'b0111111111;


always @(*) begin
    casex(comp)
        19'bxxxxxxxxxxxxxxxxxx1:    value = 12'b011000001111;
        19'bxxxxxxxxxxxxxxxxx10:    value = 12'b010111111101;
        19'bxxxxxxxxxxxxxxxx10x:    value = 12'b010111101011;
        19'bxxxxxxxxxxxxxxx10xx:    value = 12'b010111011010;
        19'bxxxxxxxxxxxxxx10xxx:    value = 12'b010111001000;
        19'bxxxxxxxxxxxxx10xxxx:    value = 12'b010110110111;
        19'bxxxxxxxxxxxx10xxxxx:    value = 12'b010110100110;
        19'bxxxxxxxxxxx10xxxxxx:    value = 12'b010110011000;
        19'bxxxxxxxxxx10xxxxxxx:    value = 12'b010110011011;
        19'bxxxxxxxxx10xxxxxxxx:    value = 12'b010110101101;
        19'bxxxxxxxx10xxxxxxxxx:    value = 12'b010110111111;
        19'bxxxxxxx10xxxxxxxxxx:    value = 12'b010111010001;
        19'bxxxxxx10xxxxxxxxxxx:    value = 12'b010111100011;
        19'bxxxxx10xxxxxxxxxxxx:    value = 12'b010111110101;
        19'bxxxx10xxxxxxxxxxxxx:    value = 12'b011000000111;
        19'bxxx10xxxxxxxxxxxxxx:    value = 12'b011000011001;
        19'bxx10xxxxxxxxxxxxxxx:    value = 12'b011000101100;
        19'bx10xxxxxxxxxxxxxxxx:    value = 12'b011000111110;
        19'b10xxxxxxxxxxxxxxxxx:    value = 12'b011001001110;
        default:	value = 12'b011001001110;
    endcase
end

endmodule
