from NlDefine import NLOperation

from lut_make import range_lut_make
from appr_test import vis_dif, vis_hw
from hdl_emit import verilog_emit, testbench_emit


NLOperation.range_lut_make = range_lut_make
NLOperation.vis_dif = vis_dif
NLOperation.vis_hw = vis_hw

NLOperation.verilog_emit = verilog_emit
NLOperation.testbench_emit = testbench_emit


if __name__ == '__main__':
    # nlf = NLOperation(config = 'template/example.ini')
    nlf = NLOperation(config = 'output/example.ini')
    # lut, acc = nlf.range_lut_make()
    # print(lut)
    # print(len(lut), acc)

    # lut_neg, acc_neg = nlf.range_lut_make(neg=True)
    # print(lut_neg)
    # print(len(lut_neg), acc_neg)

    nlf.vis_dif()

    # nlf.range_lut_emit()
    # nlf.range_lut_emit(neg=True)

    # print(pwl_hdl_generate(nlf))
    # top_hdl_emit(nlf)

    # nlf.verilog_emit()
    # nlf.testbench_emit()

    # nlf.vis_hw()
