# Emit the Verilog File of Generated Non-linear Function Operator

import re
import numpy as np
from NlDefine import NLOperation
from utils import dec_to_bin
from lut_emit import range_lut_emit


def pwl_hdl_generate_reg(self:NLOperation) -> str:
    kbit = self.KEY_BIT
    ipoi = self.IPOI
    wbit = self.WORD_BIT
    opoi = self.OPOI

    seg_num = self.tfunc.tpwl.seg_number
    linear_list = self.tfunc.tpwl.linears

    pwl_hdl = ''
    # Create if-else sequence
    for index in range(seg_num):
        # comparison expression
        pwl_hdl = pwl_hdl + '    ' # indent
        if index != 0:
            pwl_hdl = pwl_hdl + 'else '
        
        linear = linear_list[index]
        left_bound = linear.boundry_l > -(2**ipoi)
        right_bound = linear.boundry_r < 2**ipoi

        comp_l = ''
        and_flag = ''
        comp_r = ''
        if left_bound:
            bstr = dec_to_bin(linear.boundry_l, bits=kbit, poi=ipoi)
            comp_l = 'in_reg >= $signed({}\'b{})'.format(kbit, bstr)
        
        if left_bound and right_bound:
            and_flag = ' && '
        
        if right_bound:
            bstr = dec_to_bin(linear.boundry_r, bits=kbit, poi=ipoi)
            comp_r = 'in_reg < $signed({}\'b{})'.format(kbit, bstr)

        pwl_hdl = pwl_hdl + 'if ({}{}{})\n'.format(comp_l, and_flag, comp_r)

        # assignment expression
        flat = (linear.slope == 0)
        incl = (linear.slope != 0) and (linear.bias == 0) # bias=0 -> saving adder resources
        
        if not flat and not incl:
            raise ValueError('Illegal Linear Function!')
        
        if flat:
            bstr = dec_to_bin(linear.bias, bits=wbit, poi=opoi)
            assign_str = '{}\'b{}'.format(wbit, bstr)
        
        if incl:
            greater_zero = (linear.slope >=0)
            if greater_zero:
                signal_process = 'in_reg'
            else:
                signal_process = '(~in_reg + 1\'b1)'

            shift_num = int(np.log2(abs(linear.slope)))
            spoi = ipoi + shift_num

            # Pending for modification
            index_shead = (kbit-2) - (spoi-opoi)
            if index_shead < 0 :
                raise ValueError('Out-of-Range Piecewise Matching!')
            
            padding_head = ''
            if index_shead > kbit-2:
                padding_head_num = index_shead - (kbit-2)
                padding_head = '{' + str(padding_head_num)+ '{' + '{}[{}]'.format(signal_process, kbit-1) + '}'+'}, '
                index_stail = kbit-2

            index_stail = (kbit-wbit) - (spoi-opoi)
            padding_tail = ''
            if index_stail < 0:
                padding_tail_num = abs(index_stail)
                padding_tail = ', {}\'b0'.format(padding_tail_num)
                index_stail = 0
            
            assign_str = '{' + '{}[{}], '.format(signal_process, kbit-1)
            assign_str = assign_str + padding_head
            assign_str = assign_str + '{}[{}:{}]'.format(signal_process, index_shead, index_stail)
            assign_str = assign_str + padding_tail
            assign_str = assign_str + '}'
        
        pwl_hdl = pwl_hdl + '        ' #indent
        pwl_hdl = pwl_hdl + 'pwl_val <= {};\n'.format(assign_str)
    
    default = str(wbit)+'{' + '1\'b0' + '}'
    pwl_hdl = pwl_hdl + '    else\n        ' # indent
    pwl_hdl = pwl_hdl + 'pwl_val <= {};'.format(default)

    return pwl_hdl        


def pwl_hdl_generate(self:NLOperation) -> str:
    kbit = self.KEY_BIT
    ipoi = self.IPOI
    wbit = self.WORD_BIT
    opoi = self.OPOI

    seg_num = self.tfunc.tpwl.seg_number
    linear_list = self.tfunc.tpwl.linears

    pwl_hdl = ''

    # Create if-else sequence
    for index in range(seg_num):
        # indent
        if index != 0:
            pwl_hdl = pwl_hdl + '                 '
        
        linear = linear_list[index]
        left_bound = linear.boundry_l > -(2**ipoi)
        right_bound = linear.boundry_r < 2**ipoi

        comp_l = ''
        and_flag = ''
        comp_r = ''
        if left_bound:
            bstr = dec_to_bin(linear.boundry_l, bits=kbit, poi=ipoi)
            comp_l = 'in_reg >= $signed({}\'b{})'.format(kbit, bstr)
        
        if left_bound and right_bound:
            and_flag = ' && '
        
        if right_bound:
            bstr = dec_to_bin(linear.boundry_r, bits=kbit, poi=ipoi)
            comp_r = 'in_reg < $signed({}\'b{})'.format(kbit, bstr)
        
        pwl_hdl = pwl_hdl + ' ({}{}{}) ? '.format(comp_l, and_flag, comp_r)


        # assignment expression
        flat = (linear.slope == 0)
        incl = (linear.slope != 0) and (linear.bias == 0) # bias=0 -> saving adder resources
        
        if not flat and not incl:
            raise ValueError('Illegal Linear Function!')
        
        if flat:
            bstr = dec_to_bin(linear.bias, bits=wbit, poi=opoi)
            assign_str = '{}\'b{}'.format(wbit, bstr)
        
        if incl:
            greater_zero = (linear.slope >=0)
            if greater_zero:
                signal_process = 'in_reg'
            else:
                signal_process = '(~in_reg + 1\'b1)'

            shift_num = int(np.log2(abs(linear.slope)))
            spoi = ipoi + shift_num

            # Pending for modification
            index_shead = (kbit-2) - (spoi-opoi)
            if index_shead < 0 :
                raise ValueError('Out-of-Range Piecewise Matching!')
            
            padding_head = ''
            if index_shead > kbit-2:
                padding_head_num = index_shead - (kbit-2)
                padding_head = '{' + str(padding_head_num)+ '{' + '{}[{}]'.format(signal_process, kbit-1) + '}'+'}, '
                index_stail = kbit-2

            index_stail = (kbit-wbit) - (spoi-opoi)
            padding_tail = ''
            if index_stail < 0:
                padding_tail_num = abs(index_stail)
                padding_tail = ', {}\'b0'.format(padding_tail_num)
                index_stail = 0
            
            assign_str = '{' + '{}[{}], '.format(signal_process, kbit-1)
            assign_str = assign_str + padding_head
            assign_str = assign_str + '{}[{}:{}]'.format(signal_process, index_shead, index_stail)
            assign_str = assign_str + padding_tail
            assign_str = assign_str + '}'

        pwl_hdl = pwl_hdl + '{} :\n'.format(assign_str)

    default = str(wbit)+'{' + '1\'b0' + '}'
    pwl_hdl = pwl_hdl + '                  {' + default + '};\n'

    return pwl_hdl


# for more robust usage, the left and right markers should be different 
def replace_para(input_file, output_file, parameters, 
                        marker_l='$$', marker_r='$$'):
    # Read
    with open(input_file, 'r') as file:
        content = file.read()

    # Replace
    for key, value in parameters.items():
        pattern = re.escape(marker_l) + r'\s*' + re.escape(key) + r'\s*' + re.escape(marker_r)
        content = re.sub(pattern, str(value), content)

    # Write
    with open(output_file, 'w') as file:
        file.write(content)



def top_hdl_emit(self:NLOperation, 
                template:str='template/raw.v', 
                path:str='output/') -> None:

    paras = {
        'FUNC': self.label,
        'INPUT_BIT': self.INPUT_BIT,
        'OUTPUT_BIT': self.OUTPUT_BIT,
        'KEY_BIT': self.KEY_BIT,
        'WORD_BIT': self.WORD_BIT,

        'PWL_HDL': None
    }


    PWL = pwl_hdl_generate(self)
    paras['PWL_HDL'] = PWL
    
    outfile = path + 'top.v'

    replace_para(input_file=template, output_file=outfile,
                        parameters=paras,
                        marker_l='$$', marker_r='$$')
    
    print(f"Parameters in {template} have been modified and saved to {outfile}")
    return



def verilog_emit(self:NLOperation, template:str='template/raw.v', path:str='output/'):

    print(f" Verilog HDL Generation Starts ".center(60, '*'))

    top_hdl_emit(self, template, path)
    print(f"Top module of DIF-LUT Approximation has successfully generated.\n")

    range_lut_emit(self, neg=False, path=path)
    range_lut_emit(self, neg=True, path=path)
    print(f"Range-addressable look-up tables have successfully generated.\n")

    print(f" Verilog HDL Generation Done ".center(60, '*'))

    return



def testbench_emit(self:NLOperation, template:str='template/rawtb.v', path:str='output/') -> None:
    paras = {
        'FUNC': self.label,
        'INPUT_BIT': self.INPUT_BIT,
        'OUTPUT_BIT': self.OUTPUT_BIT,
        'INPUT_NUM': 2**self.INPUT_BIT,

        'OUTPUT_FILE': r'"D:\\\\GitLife\\\\DIF-LUT-TOOL\\\\output\\\\simresult.txt"'
        # 'OUTPUT_FILE': r'"simresult.txt"'
    }

    outfile = path + 'top_tb.v'
    replace_para(input_file=template, output_file=outfile,
                        parameters=paras,
                        marker_l='$$', marker_r='$$')
    
    print(f"Parameters in {template} have been modified and saved to {outfile}")
    return