# Emit the Verilog File of Generated Look-Up Table

from NlDefine import NLOperation


def range_lut_emit(self:NLOperation, neg:bool=False, path:str='output/') -> None:

    lut, pre_limit = self.range_lut_make(neg=neg)

    if not neg: # positive plane
        value_b = sorted(lut.items(), key=lambda x:x[0][1])[-1][1] # Boundary Value
        fname = path + 'dif_lut_K{}W{}.v'.format(self.KEY_BIT, self.WORD_BIT)
        mname = 'dif_lut_K{}W{}'.format(self.KEY_BIT, self.WORD_BIT)
    else: # negative plane
        value_b = sorted(lut.items(), key=lambda x:x[0][0])[-1][1] # Boundary Value
        fname = path + 'dif_lut_K{}W{}_sym.v'.format(self.KEY_BIT, self.WORD_BIT)
        mname = 'dif_lut_K{}W{}_sym'.format(self.KEY_BIT, self.WORD_BIT)
        

    with open(fname, 'w') as f:

        f.write('// @ KEY_BIT={}\t WORD_BIT={}\n'.format(self.KEY_BIT, self.WORD_BIT))

        f.write('module {} (\n'.format(mname))
        f.write('    input signed [{}:0]     key,\n'.format(self.KEY_BIT-1))
        f.write('    output signed [{}:0]    value\n'.format(self.WORD_BIT-1))
        f.write(');\n\n')

        seg_num = len(lut)
        f.write('wire [{} : 0] comp;\n'.format(seg_num-1))
        f.write('reg  [{} : 0] value;\n\n'.format(self.WORD_BIT-1))

        if not neg:
            for i, key in enumerate(lut.keys()):
                f.write('assign comp[{}] = key < {}\'b{};\n'.format(i, self.KEY_BIT, key[1]))
        else:
            for i, key in enumerate(lut.keys()):
                f.write('assign comp[{}] = key > {}\'b{};\n'.format(i, self.KEY_BIT, key[1]))    


        f.write('\n\n')

        f.write('always @(*) begin\n')
        f.write('    casex(comp)\n')

        for i, (key, value) in enumerate(lut.items()):
            s_front = (seg_num-i-1)*'x' + '1'
            if i == 0:
                s_back = ''
            else:
                s_back = '0' + (i-1) * 'x'
            s = s_front + s_back
            f.write('        {}\'b{}:    value = {}\'b{};\n'.format(seg_num, s, self.WORD_BIT, value))

        f.write('        default:	value = {}\'b{};\n'.format(self.WORD_BIT, value_b))
        f.write('    endcase\n')
        f.write('end\n\n')

        f.write('endmodule\n')

