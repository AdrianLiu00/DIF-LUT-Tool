# Visual and Analytical Test of Approximation

from utils import dec_to_bin, bin_to_dec, look_up
import matplotlib.pylab as plt

from NlDefine import NLOperation


def vis_dif(self:NLOperation, lut_pair:tuple[tuple[dict, float], tuple[dict, float]]) -> None:
    '''lut_pair : (lut_pos, lut_neg)'''
    
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
            cut_appr = bin_to_dec(look_up(in_table[i], lut_pair[0], self.KEY_BIT), poi=self.OPOI)
        else:
            cut_appr = bin_to_dec(look_up(in_table[i], lut_pair[1], self.KEY_BIT), poi=self.OPOI)
        
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

