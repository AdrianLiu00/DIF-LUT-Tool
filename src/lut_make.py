from utils import dec_to_bin, bin_to_dec, quantize, inv

from NlDefine import NLOperation
from FuncRe import PiecewiseL
from FuncZoo import tpwl_sigmoid

from typing import Callable
import numpy as np

def err_qunt_pwl(pwl:PiecewiseL, keybit:int, poi:int) -> Callable:
    '''return the err func: (pwl_hw - pwl_tru)'''

    linear_list = pwl.linears
    linear_list = sorted(linear_list, key=lambda x: x.boundry_l)

    def epwl(x:float) -> float:

        for linear in linear_list:
            if x >= linear.boundry_l and x < linear.boundry_r:
                err1 = linear.slope * (-(2**(poi-keybit))) # no rounding error
                err2 = quantize(linear.bias, keybit, poi)[0] - linear.bias
                return err1 + err2

        raise ValueError('Illegal Piecewise or Out-of-bounds Input!')

    return epwl


def range_lut_make(self:NLOperation, neg:bool=False) -> tuple[dict, float]:
        
    key_table = []

    if not neg:
        for i in range(2**(self.KEY_BIT-1)):
            dec_num = i / (2**(self.KEY_BIT - self.IPOI - 1))
            key_table.append(dec_to_bin(dec_num, bits=self.KEY_BIT, poi=self.IPOI))
    else:
        for i in range(2**(self.KEY_BIT-1)):
            dec_num = -i / (2**(self.KEY_BIT - self.IPOI - 1))
            key_table.append(dec_to_bin(dec_num, bits=self.KEY_BIT, poi=self.IPOI))

    # epwl = err_qunt_pwl(self.tfunc.tpwl, self.KEY_BIT, self.IPOI)
    # epwl = err_qunt_pwl(self.tfunc.tpwl, self.INPUT_BIT, self.IPOI)
    # dif_hw = lambda x : self.tfunc.dif(x) - epwl(x)
    dif_hw = lambda x : self.tfunc.dif(x) # Old version
    
    dense_table = []
    for i in range(len(key_table)):
        dense_table.append(dif_hw(bin_to_dec(key_table[i], poi=self.IPOI)))

    dif_table_ori = [abs(dense_table[i+1] - dense_table[i]) for i in range(len(dense_table) - 1)]
    # print(dif_table_ori)
    # print('Max Dense Dif:  ', max(dif_table_ori))
    
    print('LIMIT PRESION:  {:.5f}'.format(max(dif_table_ori)/2))
    # print('TARGET PRESION:  {:.4f}'.format(PRE))


    bound_table = []
    dif_table = []
    
    if not neg:
        bound_table.append(key_table[0])
    else:
        bound_table.append(key_table[1]) # avoid 0 in negtive lut
    
    index = 0
    while index < len(dif_table_ori):
        dif_sum = 0
        while True:
            if(index == len(dif_table_ori)):
                break
            if(dif_sum + dif_table_ori[index] > self.BAND):
                break
            dif_sum = dif_sum + dif_table_ori[index]
            index = index + 1
        bound_table.append(key_table[index])
        dif_table.append(dif_sum)

    if neg: # Negative Boundary Correction
        bound_table[-1] = '1' + '0' * (self.KEY_BIT-1)

    # print(len(bound_table), bound_table)
    # print(len(dif_table), dif_table)


    word_table = []
    for i in range(len(bound_table) - 1):
        result = 0.5 * (dif_hw(bin_to_dec(bound_table[i], poi=self.IPOI)) + dif_hw(bin_to_dec(bound_table[i+1], poi=self.IPOI)))
        _, word = quantize(result, bits=self.WORD_BIT, poi=self.OPOI)
        word_table.append(word)
        print(result)
    print(word_table)

    lut = {}
    for i in range(len(word_table)):
        lut[(bound_table[i], bound_table[i+1])] = word_table[i]
    
    accuracy_limit = max(dif_table_ori)/2

    return lut, accuracy_limit


# NOT UPGRADE YET!!
def sym_lut_make(self:NLOperation, lut:dict) -> dict:
    lut_sym = {}
    sat_code = '1' + '0'* (self.OUTPUT_BIT-1)

    for (key, value) in lut.items():
        # Invert-Key
        key_s0 = inv(key[0], self.KEY_BIT)
        key_s1 = inv(key[1], self.KEY_BIT)

        # Symmetry-Value
        value_dec = int(value, 2)
        value_dec_s = int(sat_code,2) - value_dec
        value_s = bin(value_dec_s)[2:]
        value_s = '0' * (self.OUTPUT_BIT - len(value_s)) + value_s

        lut_sym[(key_s0, key_s1)] = value_s
    
    return lut_sym



if __name__ == '__main__':
    epwl = err_qunt_pwl(tpwl_sigmoid, 10, 3)
    print(epwl(-4))