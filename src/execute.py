from NlImpl import NLOperation

def run(config = 'template/config.ini'):
    nlf = NLOperation(config)
    nlf.verilog_emit()
    nlf.testbench_emit()

    if nlf.VIS:
        nlf.vis_dif()

    return

if __name__ == "__main__":
    run(config = 'template/config.ini')