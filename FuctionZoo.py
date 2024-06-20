import numpy as np

from typing import Dict


class Func():
    ori = None
    pwl = None
    dif = None

    def __init__(self, fori, fpwl) -> None:
        self.ori = fori
        self.pwl = fpwl
        self.dif = lambda x : fori(x) - fpwl(x)
        return


# =================================================================================
# Function Examples

# --------------------------------------------------
def sin(x):
    return np.sin(x)

def pwl_sin(x):
    if x >= 1:
        return 1
    if x < 1 and x > -1:
        return x
    if x <= -1:
        return -1

# --------------------------------------------------
def cos(x):
    return np.cos(x)


def pwl_cos(x):
    # segments:[pi/6, 2] -> [0.5234375(0.1000011), 2]
    bound = 0.5234375 # pi/6 in 8Q1

    if x >= bound and x <= 2:
        return -x
    if x <= -bound and x >= -2:
        return x
    if x >= -bound and x <= bound:
        return -bound

# --------------------------------------------------
def tanh(x):
    return (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))

def pwl_tanh(x):
    if x >= 1:
        return 1
    if x < 1 and x > -1:
        return x
    if x <= -1:
        return -1

# --------------------------------------------------
def sigmoid(x):
    return 1/(1 + np.exp(-x))

def pwl_sigmoid(x):
    if x >= 2:
        return 0.5
    if x < 2 and x > -2:
        return x * 0.25
    if x <= -2:
        return -0.5

# --------------------------------------------------
def elu(x):
    if x >= 0:
        return x
    else:
        return np.exp(x)-1

def pwl_elu(x):
    if x <= -1:
        return -1
    else:
        return x

# --------------------------------------------------
def silu(x):
    return x * sigmoid(x)

def pwl_silu(x):
    if x >= 0:
        return x
    else:
        return 0


# =================================================================================
# Function Zoo Arrangement

FuncZoo : Dict[str, Func] = {
    'sin' : Func(sin, pwl_sin),
    'cos' : Func(cos, pwl_cos),
    'tanh' : Func(tanh, pwl_tanh),
    'sigmoid' : Func(sigmoid, pwl_sigmoid),
    'elu' : Func(elu, pwl_elu),
    'silu' : Func(silu, pwl_silu)
}



if __name__ == '__main__':
    print(FuncZoo['sin'].dif(1))
    print(FuncZoo['elu'].dif(-1))


