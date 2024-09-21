# Visual and Analytical Test of Approximation

import matplotlib.pylab as plt
import numpy as np

from NlDefine import NLOperation
from utils import dec_to_bin, bin_to_dec, look_up



def vis_dif(self:NLOperation) -> None:
    '''lut_pair : (lut_pos, lut_neg)'''
    
    lut_pos, acc_pos = self.range_lut_make()
    lut_neg, acc_neg = self.range_lut_make(neg=True)

    bias = 2 ** (self.IPOI)

    in_table = []
    in_table_dec = []
    for i in range(2**self.INPUT_BIT):
        dec_num = i/ (2**(self.INPUT_BIT - self.IPOI -1)) - bias
        in_table_dec.append(dec_num)
        in_table.append(dec_to_bin(dec_num, bits=self.INPUT_BIT, poi=self.IPOI))
    in_table = in_table[:-1]
    in_table_dec = in_table_dec[:-1]

    cut_appr_table = []
    cut_tru_table = []
    cut_err_table = []

    appr_table = []
    tru_table = []
    err_table = []
    for i in range(len(in_table)):
        tru = self.tfunc.ori(in_table_dec[i])
        
        if in_table[i][0] == '0':
            cut_appr = bin_to_dec(look_up(in_table[i], lut_pos, self.KEY_BIT), poi=self.OPOI)
        else:
            cut_appr = bin_to_dec(look_up(in_table[i], lut_neg, self.KEY_BIT), poi=self.OPOI)
        
        pwl_appr = self.tfunc.pwl(bin_to_dec(in_table[i], poi= self.IPOI))
        appr = pwl_appr + cut_appr
        err = appr - tru
        tru_table.append(tru)
        appr_table.append(appr)
        err_table.append(err)

        cut_tru = self.tfunc.dif(in_table_dec[i])
        cut_err = cut_appr - cut_tru
        cut_appr_table.append(cut_appr)
        cut_tru_table.append(cut_tru)
        cut_err_table.append(cut_err)

    print(max(cut_err_table), min(cut_err_table))
    print(max(err_table), min(err_table))

    plt.subplot(2, 2, 1)
    plt.title('KEY_BIT: {}'.format(self.KEY_BIT))
    plt.plot(in_table_dec, cut_tru_table, color= 'green', linewidth=2.5)
    plt.plot(in_table_dec, cut_appr_table, color = 'blue', linewidth=2.5)

    plt.subplot(2, 2, 2)
    plt.title('KEY_BIT: {}'.format(self.KEY_BIT))
    plt.plot(in_table_dec, tru_table, color= 'green', linewidth=2.5)
    plt.plot(in_table_dec, appr_table, color = 'blue', linewidth=2.5)

    plt.subplot(2, 2, 3)
    plt.title('MAX_ERROR: POS -{:.5f}  NEG -{:.5f}'.format(max(cut_err_table), min(cut_err_table)))
    plt.plot(in_table_dec, cut_err_table, color='red')
    plt.axhline(y=max(cut_err_table), linewidth=1.5, color='#668B8B', linestyle='--')
    plt.axhline(y=min(cut_err_table), linewidth=1.5, color='#668B8B', linestyle='--')


    plt.subplot(2, 2, 4)
    plt.title('MAX_ERROR: POS -{:.5f}  NEG -{:.5f}'.format(max(err_table), min(err_table)))
    plt.plot(in_table_dec, err_table, color='red')
    plt.axhline(y=max(err_table), linewidth=1.5, color='#668B8B', linestyle='--')
    plt.axhline(y=min(err_table), linewidth=1.5, color='#668B8B', linestyle='--')

    plt.show()

    return


def vis_hw(self:NLOperation, path:str='output/simresult.txt') -> None:

    frac_in = self.INPUT_BIT -1 -self.IPOI
    frac_out = self.OUTPUT_BIT -1 -self.OPOI

    vector_in = []
    vector_out = []

    with open(path, 'r') as file:
        for line in file.readlines():
            if(line == '\n'):
                continue
            if(line[0:2] == 'in'):
                instr = line[3:].strip('\n')
                vector_in.append(bin_to_dec(instr, poi=self.IPOI))
            if(line[0:3] == 'out'):
                outstr = line[4:].strip('\n')
                vector_out.append(bin_to_dec(outstr, poi=self.OPOI))

    func = self.tfunc.ori

    # print(len(vector_in), len(vector_out))

    

    vector_tru = [func(x) for x in vector_in]
    err = [vector_out[i] - vector_tru[i] for i in range(len(vector_in))]

    
    # Sort
    vectors = [(vector_in[i], vector_out[i], vector_tru[i], err[i]) for i in range(len(vector_in))]
    vectors = sorted(vectors, key=lambda x : x[0])
    
    vectors = vectors[self.QMARGIN:-self.QMARGIN]

    vector_in = [item[0] for item in vectors]
    vector_out = [item[1] for item in vectors]
    vector_tru = [item[2] for item in vectors]
    err = [item[3] for item in vectors]
    err_abs = [abs(i) for i in err]

    for _, e in enumerate(err_abs):
        if e > 0.2:
            print(dec_to_bin(vector_in[_], self.INPUT_BIT, self.IPOI))


    # print(max(err), err.index(max(err)))
    # print(min(err), err.index(min(err)))
    print('Mean Absolute Error of Approximation: {:.8f}'.format(np.mean(err_abs)))
    print('ERROR Range:    [{:.9f} , {:.9f}]'.format(max(err), min(err)))


    plt.subplot(2, 1, 1)
    plt.plot(vector_in, vector_tru, color= 'green', linewidth=5)
    plt.plot(vector_in, vector_out, color = 'blue', linewidth=2.8)

    plt.subplot(2, 1, 2)
    plt.title('ERROR Range:    [{:.5f} , {:.5f}]'.format(max(err), min(err)))

    plt.plot(vector_in, err, color='red')
    plt.axhline(y=max(err), linewidth=1.5, color='#668B8B', linestyle='--')
    plt.axhline(y=min(err), linewidth=1.5, color='#668B8B', linestyle='--')
    plt.show()

