import scipy.special
import random
from hypotheses.sign_statistics import *


# input: alpha and statistic k = k_2 + k_3
# output: threshold c2
def threshold_c_right(alpha, k) -> int:
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


# input: alpha and statistic k = k_2 + k_3
# output: threshold c1
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

    # input: 3 indexes of stocks, matrix of returns of stocks, alpha
    # output: 1 - if hypothesis H_i,j,k is rejected, 0 - otherwise
    def one_sided_test_ijk(self, i, j, k, kind='not_rand'):
        k2 = stat_T2(self.ret_inds, i, j, k)
        k3 = stat_T3(self.ret_inds, i, j, k)
        c_r = threshold_c_right(self.alpha, k2 + k3)
        if kind == 'rand' and k2 == c_r:
            return random.randint(0, 1)
        elif kind == 'max' and k2 == c_r:
            if k2 == k3:
                return random.randint(0, 1)
            else:
                return k2 > k3
        return k2 >= c_r

    def two_sided_test_ijk(self, i, j, k, kind='rand'):
        k2 = stat_T2(self.ret_inds, i, j, k)
        k3 = stat_T3(self.ret_inds, i, j, k)
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


    def one_sided_test_ijkl(self, i, j, k, l, ret_inds, alpha):
        k2 = stat_R2(ret_inds, i, j, k, l)
        k3 = stat_R3(ret_inds, i, j, k, l)
        k = k2 + k3
        c2 = threshold_c_right(alpha, k)
        # if k2 == c2:
        #   # print('test_ijkl, random')
        #   return random.randint(0, 1)
        return k2 >= c2


    def complex_rand_test_ijkl(i, j, k, l, ret_inds, alpha):
        k2 = stat_R2(ret_inds, i, j, k, l)
        k3 = stat_R3(ret_inds, i, j, k, l)
        k = k2 + k3
        c1 = threshold_c_left(alpha, k)
        c2 = threshold_c_right(alpha, k)
        if k2 > c2:
            return 1
        if k2 < c1:
            return 0
        return random.randint(0, 1)


    def complex_max_test_ijkl(i, j, k, l, ret_inds, alpha):
        k2 = stat_T2(ret_inds, i, j, k)
        k3 = stat_T3(ret_inds, i, j, k)
        k = k2 + k3
        c1 = threshold_c_left(alpha, k)
        c2 = threshold_c_right(alpha, k)
        if k2 > c2:
            return 1
        if k2 < c1:
            return 0
        if k2 == k3:
            return random.randint(0, 1)
        else:
            return k2 > k3
