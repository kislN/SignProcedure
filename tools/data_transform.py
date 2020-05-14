import numpy as np


def get_returns(prices):
    returns = []
    for day in range(len(prices) - 1):
        returns.append(np.log(prices[day + 1] / prices[day]))
    return returns

def get_norm_seq(matrix, N):
  return np.random.multivariate_normal(mean=np.zeros(len(matrix[0])), cov=matrix, size=N).T

def get_indicators(returns):
  inds = []
  for ret in returns:
    if (ret > 0):
      inds.append(1)
    else:
      inds.append(0)
  return inds

def get_inds_matrix(returns):
  ret_inds = []
  for stock in returns:
    ret_inds.append(get_indicators(stock))
  return ret_inds

# def get_sign_coef(stock_1, stock_2):
#   count = 0
#   for t in range(len(stock_1)):
#     if (stock_1[t] == stock_2[t]):
#       count += 1
#   return count
#
# def get_coef_matrix(ret_inds):
#   sign_coef_matrix = []
#   for i in range(len(ret_inds)):
#     sign_coef_matrix.append([])
#     for j in range(len(ret_inds)):
#       sign_coef_matrix[i].append(get_sign_coef(ret_inds[i], ret_inds[j]))
#   return sign_coef_matrix

