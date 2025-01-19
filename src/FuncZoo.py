import numpy as np
from scipy.special import erf

from typing import Dict
from FuncRe import Linear, PiecewiseL, Func


# =================================================================================
# Function Examples

INF = 999

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

tpwl_sin = PiecewiseL(3,[
    Linear(-INF, -1, 0, -1),
    Linear(-1, 1, 1, 0),
    Linear(1, INF, 0, 1)
])

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

tpwl_cos = PiecewiseL(3,[
    Linear(-INF, -0.5234375, 1, 0),
    Linear(-0.5234375, 0.5234375, 0, -0.5234375),
    Linear(0.5234375, INF, -1, 0)
])

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

tpwl_tanh = PiecewiseL(3,[
    Linear(-INF, -1, 0, -1),
    Linear(-1, 1, 1, 0),
    Linear(1, INF, 0, 1)
])

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

tpwl_sigmoid = PiecewiseL(3,[
    Linear(-INF, -2, 0, -0.5),
    Linear(-2, 2, 0.25, 0),
    Linear(2, INF, 0, 0.5)
])

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

tpwl_elu = PiecewiseL(2,[
    Linear(-INF, -1, 0, -1),
    Linear(-1, INF, 1, 0)
])

# --------------------------------------------------
def silu(x):
    return x * sigmoid(x)

def pwl_silu(x):
    if x >= 0:
        return x
    else:
        return 0

tpwl_silu = PiecewiseL(2,[
    Linear(-INF, 0, 0, 0),
    Linear(0, INF, 1, 0)
])

# --------------------------------------------------
def gelu(x):
    return 0.5 * x * (1 + erf(x / np.sqrt(2)))

def deri_gelu(x):
    phi_x = 0.5 * (1 + erf(x / np.sqrt(2)))
    pdf_x = np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
    return phi_x + x * pdf_x

def pwl_gelu(x):
    if x >= 0:
        return x
    else:
        return 0

tpwl_gelu = PiecewiseL(2,[
    Linear(-INF, 0, 0, 0),
    Linear(0, INF, 1, 0)
])

# --------------------------------------------------
def exp_minus_x(x):
    if x>=0:
        return np.exp(-x)
    else:
        return 1

def pwl_exp_minus_x(x):
    if x >= 0.69:
        return -0.69
    if x <=0:
        return 1
    return -x

tpwl_exp_minus_x = PiecewiseL(3,[
    Linear(-INF, 0, 0, 0),
    Linear(0, 0.69, -1, 0),
    Linear(0.69, INF, 0, -0.69)
])

# =================================================================================
# Function Zoo Arrangement

NLFuncZoo : Dict[str, Func] = {
    'sin' : Func(sin, tpwl_sin),
    'cos' : Func(cos, tpwl_cos),
    'tanh' : Func(tanh, tpwl_tanh),
    'sigmoid' : Func(sigmoid, tpwl_sigmoid),
    'elu' : Func(elu, tpwl_elu),
    'silu' : Func(silu, tpwl_silu),
    'gelu' : Func(gelu, tpwl_gelu),
    'exp_-x' : Func(exp_minus_x, tpwl_exp_minus_x)
}



if __name__ == '__main__':
    print(NLFuncZoo['sin'].dif(1))
    print(NLFuncZoo['elu'].dif(-1))


