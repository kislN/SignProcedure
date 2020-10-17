import scipy.special
import random
from hypotheses.sign_statistics import *


def threshold_c_right(alpha, k):
    c = 0
    while True:
        _sum = 0
        for i in range(c, k + 1):
            _sum += scipy.special.binom(k, i)
        _sum *= 1 / 2 ** k
        if _sum <= alpha:
            break
        else:
            c += 1
    return c


def threshold_c_left(alpha, k) -> int:
    c = k + 1
    while True:
        _sum = 0
        for i in range(0, c):
            _sum += scipy.special.binom(k, i)
        _sum *= 1 / 2 ** k
        if _sum <= alpha:
            break
        else:
            c -= 1
    return c


class Test:
    def __init__(self, alpha, ret_inds):
        self.alpha = alpha
        self.ret_inds = ret_inds

    def one_sided(self, compared_stocks, kind='not_rand'):
        if len(compared_stocks) == 3:
            k2 = stat_T2(self.ret_inds, compared_stocks)
            k3 = stat_T3(self.ret_inds, compared_stocks)
        else:
            k2 = stat_R2(self.ret_inds, compared_stocks)
            k3 = stat_R3(self.ret_inds, compared_stocks)
        k = k2 + k3
        c_r = threshold_c_right(self.alpha, k)
        if kind == 'rand' and k2 == c_r:
            return random.randint(0, 1)
        elif kind == 'max' and k2 == c_r:
            if k2 == k3:
                return random.randint(0, 1)
            else:
                return k2 > k3
        return k2 >= c_r

    def two_sided(self, compared_stocks, kind='rand'):
        if len(compared_stocks) == 3:
            k2 = stat_T2(self.ret_inds, compared_stocks)
            k3 = stat_T3(self.ret_inds, compared_stocks)
        else:
            k2 = stat_R2(self.ret_inds, compared_stocks)
            k3 = stat_R3(self.ret_inds, compared_stocks)
        c_l = threshold_c_left(self.alpha / 2, k2 + k3)
        c_r = threshold_c_right(self.alpha / 2, k2 + k3)
        if k2 >= c_r:
            return 1
        elif k2 <= c_l:
            return 0
        if kind == 'rand':
            return random.randint(0, 1)
        elif kind == 'max':
            if k2 == k3:
                return random.randint(0, 1)
            else:
                return k2 > k3
