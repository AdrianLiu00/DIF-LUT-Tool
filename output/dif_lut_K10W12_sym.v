// @ KEY_BIT=10	 WORD_BIT=12
module dif_lut_K10W12_sym (
    input signed [9:0]     key,
    output signed [11:0]    value
);

wire [18 : 0] comp;
reg  [11 : 0] value;

assign comp[0] = key > 10'b1111010000;
assign comp[1] = key > 10'b1110111100;
assign comp[2] = key > 10'b1110101101;
assign comp[3] = key > 10'b1110100000;
assign comp[4] = key > 10'b1110010101;
assign comp[5] = key > 10'b1110001011;
assign comp[6] = key > 10'b1110000001;
assign comp[7] = key > 10'b1101111000;
assign comp[8] = key > 10'b1101101111;
assign comp[9] = key > 10'b1101100101;
assign comp[10] = key > 10'b1101011010;
assign comp[11] = key > 10'b1101001110;
assign comp[12] = key > 10'b1101000001;
assign comp[13] = key > 10'b1100110010;
assign comp[14] = key > 10'b1100100000;
assign comp[15] = key > 10'b1100001010;
assign comp[16] = key > 10'b1011101011;
assign comp[17] = key > 10'b1010100000;
assign comp[18] = key > 10'b1000000000;


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
        19'b10xxxxxxxxxxxxxxxxx:    value = 12'b011001001111;
        default:	value = 12'b011000001111;
    endcase
end

endmodule
