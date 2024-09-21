from FuncZoo import NLFuncZoo
from parser_in import read_ini, key_bit_select


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

    # Visualization
    VIS = False
    QMARGIN = 20

    # ---------------------------------------------------------------
    # Target Function

    label = 'cos'
    tfunc = NLFuncZoo[label]

    # ---------------------------------------------------------------
    def __init__(self, config='template/example.ini') -> None:
        
        # Load Parameters
        params = read_ini(config)
        self.label = params['Func']
        self.tfunc = NLFuncZoo[self.label]

        self.INPUT_BIT = int(params['Input_bitwidth'])
        self.IPOI = int(params['Input_bitwidth']) - 1 - int(params['Input_fraction_bitwidth'])
        self.OUTPUT_BIT = int(params['Output_bitwidth'])
        self.OPOI = int(params['Output_bitwidth']) - 1 - int(params['Output_fraction_bitwidth'])
        
        self.PRE = float(params['Target_Accuracy'])
        self.BAND = 2 * self.Eta * self.PRE

        self.VIS = int(params['visualize']) == 1

        # Pending for modification
        if 'Customize_Key_Bit' in params.keys():
            self.KEY_BIT = int(params['Customize_Key_Bit'])
        else:
            self.KEY_BIT = key_bit_select('template/defaultK.ini',self.label, self.PRE, self.INPUT_BIT)

        if 'Customize_Word_Bit' in params.keys():
            self.WORD_BIT = int(params['Customize_Word_Bit'])
        else:
            self.WORD_BIT = self.OUTPUT_BIT



    def range_lut_make(self, neg:bool) -> tuple[dict, float]: ...

    def verilog_emit(self, template:str, path:str) -> None: ...

    def testbench_emit(self, template:str, path:str) -> None: ...

    def vis_dif(self) -> None: ...

    def vis_hw(self, path:str='output/simresult.txt') -> None: ...



if __name__ == '__main__':
    nlf = NLOperation()
    # lut, acc = nlf.range_lut_make()
    # print(lut)


