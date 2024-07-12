from NlImpl import NLOperation

def run(config = 'template/config.ini'):
    nlf = NLOperation(config)
    nlf.verilog_emit()
    return