from typing import NamedTuple, Callable, List

# NamedTuple for Information Storage Only
# Immutable Assignments

class Linear(NamedTuple):
    boundry_l: float
    boundry_r: float
    slope: float
    bias: float


class PiecewiseL(NamedTuple):
    seg_number: int
    linears: List[Linear]


def _convert_pwl_to_func(pwl:PiecewiseL) -> Callable[[float],float]:

    linear_list = pwl.linears
    linear_list = sorted(linear_list, key=lambda x: x.boundry_l)

    def fpwl(x:float) -> float:

        for linear in linear_list:
            if x >= linear.boundry_l and x < linear.boundry_r:
                return linear.slope * x + linear.bias

        raise ValueError('Illegal Piecewise or Out-of-bounds Input!')

    return fpwl


class Func():
    # For Software Analysis - RaLUT Generation
    ori:Callable = None
    pwl:Callable = None
    dif:Callable = None

    # For Hardware Generation - HDL Emitting
    tpwl:PiecewiseL = None

    def __init__(self, fori:Callable, tpwl:PiecewiseL) -> None:
        self.ori = fori
        self.tpwl = tpwl
        self.pwl = _convert_pwl_to_func(tpwl)
        self.dif = lambda x : fori(x) - self.pwl(x)
        return




if __name__ == '__main__':
    l1 = Linear(-999, -1, 0, -1)
    l2 = Linear(-1, 1, 1, 0)
    l3 = Linear(1, 999, 0, 1)
    psin = PiecewiseL(3, [l1, l2, l3])

    print(l1)
    print(psin)

    pwl_sin = _convert_pwl_to_func(psin)
    print(pwl_sin(5))
    print(pwl_sin(0.5))
    print(pwl_sin(-2))
