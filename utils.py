import random
from turtle import color
import numpy as np
import matplotlib.pylab as plt


# Signed Binary Format:
# [1'b:sbit][poi'b:int].[frac'b:frac]
# ('1101', poi=1) -> 11.01b -> -0.75


def dec_to_bin_noround(num, bits=12, poi=0):
    # Actually the maxnum is not 2^poi
    if num > 2 ** poi or num < 0:
        return 'Incorrect Input!'
    
    bin_num = ''
    msb = 2 ** (poi-1)

    for _ in range(bits):
        if(num >= msb):
            bin_num = bin_num + '1'
            num = num - msb
        else:
            bin_num = bin_num + '0'
        num = num * 2
    
    return bin_num


def dec_to_bin(num, bits=12, poi=0) -> str:
    ''' Decimal float numer to Binary string (possibly lossy). '''

    # Determine representable boundaries
    if num >= (2**poi) or num < -(2**poi):
        return "Illegal Input."
    
    pos = (num >= 0)
    msb = 2 ** poi  # unify sign-bit
    num_com = num if num >= 0 else 2**(poi+1) + num

    # Finding the complementary code
    bin_code = ''
    for _ in range(bits):
        if(num_com >= msb):
            bin_code = bin_code + '1'
            num_com = num_com - msb
        else:
            bin_code = bin_code + '0'
        num_com = num_com * 2
    
    # Rounding
    if num_com >= msb:
        bin_code = bin(int(bin_code, 2) + 1)[2:].zfill(bits) # clear head of '0b'

    return bin_code


def bin_to_dec(bin_str, poi=0) -> float:
    ''' Binary string to Decimal float number. '''

    pos = (bin_str[0] == '0')
    bits = len(bin_str)
    frac = bits - poi - 1
    
    dec = int(bin_str, 2) / 2 ** frac if pos else (int(bin_str, 2) - 2**bits) / 2 ** frac
    
    return dec


def quantize(num, bits=12, poi=0) -> tuple[float, str]:
    ''' Obtain quantized decimal number and its binary code. '''

    bin_code = dec_to_bin(num, bits, poi)
    return bin_to_dec(bin_code, poi), bin_code


def inv_ori(bin_code) -> str :
    ''' Find the Opposite Number (signed binary). '''

    bits = len(bin_code)
    if bin_code[1:] == '0' * (bits-1): # overflow
        return '0' * bits if bin_code[0] == '0' else '0'+'1'*(bits-1)

    # inverse    
    inv_code = ''.join('1' if bit == '0' else '0' for bit in bin_code)

    # complementary
    inv_code = bin(int(inv_code, 2) + 1)[2:] # strip head string

    # sign bit extension
    sbit = '1' if bin_code[0] == '0' else '0'
    inv_code = sbit * (bits - len(inv_code)) + inv_code

    return inv_code


def inv(bin_code) -> str :
    ''' Find the Opposite Number (for signed binary string). '''

    bits = len(bin_code)
    if bin_code[1:] == '0' * (bits-1): # overflow
        return '0' * bits if bin_code[0] == '0' else '0'+'1'*(bits-1)

    inv_dec = 2**bits - int(bin_code, 2)
    inv_code = bin(inv_dec)[2:].zfill(bits)

    return inv_code



def look_up(bin_str, lut, key_bit) -> str:
    key_str = bin_str[0:key_bit]

    if key_str[0] == '0':   # Positive
        for (key, value) in lut.items():
            if key_str >= key[0] and key_str < key[1]:
                return value
        value_b = sorted(lut.items(), key=lambda x:x[0][1])[-1][1]
    
    if key_str[0] == '1':   # Negative
        for (key, value) in lut.items():
            if key_str < key[0] and key_str >= key[1]:
                return value
        value_b = sorted(lut.items(), key=lambda x:x[0][0])[-1][1]

    # Boundary Value Instead of Fixed Default Value
    return value_b



def random_test(bits=12, times=5) -> None:
    poi = random.randint(0,7)
    max_err = (0.5)**(bits-1-poi)
    print('*'*20+' Random Test Begin '+'*'*20)
    print('POI:{}\tMax Error:{}'.format(poi, max_err))

    for _ in range(times):
        seed = random.random() # seed ~ (0, 1)
        x = (2 * seed - 1) * 2**poi # x ~ (-2^poi, 2^poi)

        bin_str = dec_to_bin(x, bits, poi)
        dec = bin_to_dec(bin_str, poi)
        print("x={:.7f}\t binary={}\t dec={}\t err={:.7f}".format(x, bin_str, dec, x-dec))
        
        if abs(x-dec) > max_err:
            print('Something Wrong!!')
            print('*'*20+' Random Test Failed '+'*'*20)
            return
    
    print('*'*20+' Random Test Pass! '+'*'*20+'\n')
    return



if __name__ == '__main__':


    pai = 3.1415926
    bstr = dec_to_bin(pai/6, bits=12, poi=1)
    apai = bin_to_dec(bstr, poi=1)
    # print(pai/6, bstr, apai)

    for i in range(10):
        random_test(10)

    # print(inv('00100'))
    # print(inv('11100'))
    # print(inv('00000'))
    # print(inv('10000'))

    # print(bin_to_dec('1001', 3))

