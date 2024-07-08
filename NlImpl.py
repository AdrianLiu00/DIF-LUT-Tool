from NlDefine import NLOperation

from lut_make import range_lut_make
from lut_emit import range_lut_emit
from appr_test import vis_dif
from hdl_emit import pwl_hdl_generate, top_hdl_emit, verilog_emit

NLOperation.range_lut_make = range_lut_make
NLOperation.vis_dif = vis_dif
NLOperation.range_lut_emit = range_lut_emit
NLOperation.pwl_hdl_generate = pwl_hdl_generate
NLOperation.top_hdl_emit = top_hdl_emit
NLOperation.verilog_emit = verilog_emit


if __name__ == '__main__':
    nlf = NLOperation()
    # lut, acc = nlf.range_lut_make()
    # print(lut)
    # print(len(lut), acc)

    # lut_neg, acc_neg = nlf.range_lut_make(neg=True)
    # print(lut_neg)
    # print(len(lut_neg), acc_neg)

    # nlf.vis_dif(lut_pair=(lut, lut_neg))

    # nlf.range_lut_emit()
    # nlf.range_lut_emit(neg=True)

    # print(pwl_hdl_generate(nlf))
    # top_hdl_emit(nlf)

    nlf.verilog_emit()
