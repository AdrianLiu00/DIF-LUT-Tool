from NlDefine import NLOperation

from lut_make import range_lut_make
from appr_test import vis_dif

NLOperation.range_lut_make = range_lut_make
NLOperation.vis_dif = vis_dif


if __name__ == '__main__':
    nlf = NLOperation()
    lut, acc = nlf.range_lut_make()
    print(lut)
    print(len(lut), acc)

    lut_neg, acc_neg = nlf.range_lut_make(neg=True)
    print(lut_neg)
    print(len(lut_neg), acc_neg)

    nlf.vis_dif(lut_pair=(lut, lut_neg))
