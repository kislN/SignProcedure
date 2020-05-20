import scipy.special
import random
from hypotheses.sign_statistics import *


# input: alpha and statistic k = k_2 + k_3
# output: threshold c2
def get_threshold_c2(alpha, k):
    c = 0
    while True:
        _sum = 0
        for i in range(c, k + 1):
            _sum += scipy.special.binom(k, i)
        _sum *= 1 / 2 ** k
        # print('c = {}, _sum = {}'.format(c, _sum))
        if _sum <= alpha:
            break
        else:
            c += 1
    return c

# input: alpha and statistic k = k_2 + k_3
# output: threshold c1
def get_threshold_c1(alpha, k):
    c = k
    while True:
        _sum = 0
        for i in range(0, c):
            _sum += scipy.special.binom(k, i)
        _sum *= 1 / 2 ** k
        # print('c = {} _sum = {}'.format(c, _sum))
        if _sum <= alpha:
            break
        else:
            c -= 1
    return c

"""Tests for hypothesis H_i,j,k"""

# input: 3 indexes of stocks, matrix of returns of stocks, alpha
# output: 1 - if hypothesis H_i,j,k is rejected, 0 - otherwise
def test_ijk(i, j, k, ret_inds, alpha):
  k2 = stat_T2(ret_inds, i, j, k)
  k3 = stat_T3(ret_inds, i, j, k)
  k = k2 + k3
  c2 = get_threshold_c2(alpha, k)
  # if k2 == c2:
  #   # print('test_ijk, random')
  #   return random.randint(0, 1)
  return k2 >= c2       # if random then k2 > c2

def complex_rand_test_ijk(i, j, k, ret_inds, alpha):
  k2 = stat_T2(ret_inds, i, j, k)
  k3 = stat_T3(ret_inds, i, j, k)
  k = k2 + k3
  c1 = get_threshold_c1(alpha, k)
  c2 = get_threshold_c2(alpha, k)
  if k2 > c2:
    return 1
  if k2 < c1:
    return 0
  return random.randint(0, 1)

def complex_max_test_ijk(i, j, k, ret_inds, alpha):
  k2 = stat_T2(ret_inds, i, j, k)
  k3 = stat_T3(ret_inds, i, j, k)
  k = k2 + k3
  c1 = get_threshold_c1(alpha, k)
  c2 = get_threshold_c2(alpha, k)
  if k2 > c2:
    return 1
  if k2 < c1:
    return 0
  if k2 == k3:
    return random.randint(0, 1)
  else:
    return k2 > k3


"""Tests for hypothesis H_i,j,k,l"""

# input: 4 indexes of stocks, matrix of returns of stocks, alpha
# output: 1 - if hypothesis H_i,j,k is rejected, 0 - otherwise
def test_ijkl(i, j, k, l, ret_inds, alpha):
  k2 = stat_R2(ret_inds, i, j, k, l)
  k3 = stat_R3(ret_inds, i, j, k, l)
  k = k2 + k3
  c2 = get_threshold_c2(alpha, k)
  # if k2 == c2:
  #   # print('test_ijkl, random')
  #   return random.randint(0, 1)
  return k2 >= c2

def complex_rand_test_ijkl(i, j, k, l, ret_inds, alpha):
  k2 = stat_R2(ret_inds, i, j, k, l)
  k3 = stat_R3(ret_inds, i, j, k, l)
  k = k2 + k3
  c1 = get_threshold_c1(alpha, k)
  c2 = get_threshold_c2(alpha, k)
  if k2 > c2:
    return 1
  if k2 < c1:
    return 0
  return random.randint(0, 1)

def complex_max_test_ijkl(i, j, k, l, ret_inds, alpha):
  k2 = stat_T2(ret_inds, i, j, k)
  k3 = stat_T3(ret_inds, i, j, k)
  k = k2 + k3
  c1 = get_threshold_c1(alpha, k)
  c2 = get_threshold_c2(alpha, k)
  if k2 > c2:
    return 1
  if k2 < c1:
    return 0
  if k2 == k3:
    return random.randint(0, 1)
  else:
    return k2 > k3

