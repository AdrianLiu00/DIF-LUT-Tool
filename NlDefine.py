
from utils import dec_to_bin, bin_to_dec, quantize, inv
from utils import look_up

from FuncZoo import NLFuncZoo

class NLOperation(object):
    
    # Operation I/O Setting
    INPUT_BIT = 12
    OUTPUT_BIT = 12
    
    # RALUT Bitwidth Setting
    KEY_BIT = 10
    WORD_BIT = OUTPUT_BIT

    # # Test For activation
    # IPOI = 3 # Input point Position
    # OPOI = 0 # Output point Position

    # Test For sin/cos
    IPOI = 1 # Input point Position
    OPOI = 1 # Output point Position

    # Precision Setting
    PRE = 1e-2
    Eta = 0.9
    BAND = 2 * PRE * Eta

    QMARGIN = 20

    # ---------------------------------------------------------------
    # Target Function

    label = 'cos'
    tfunc = NLFuncZoo[label]

    # ---------------------------------------------------------------
    def __init__(self) -> None:
        pass

    def range_lut_make(self, neg:bool) -> tuple[dict, float]: ...

    def range_lut_emit(self, neg:bool, path:str) -> None: ...

    def pwl_hdl_generate(self) -> str: ...

    def top_hdl_emit(self, template:str, path:str) -> None: ...

    def verilog_emit(self, template:str, path:str) -> None: ...

    def vis_dif(self, lut_pair:tuple[tuple[dict, float], tuple[dict, float]]) -> None: ...




if __name__ == '__main__':
    nlf = NLOperation()
    # lut, acc = nlf.range_lut_make()
    # print(lut)


