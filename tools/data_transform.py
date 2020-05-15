import numpy as np

# input: list of prices of one stock for n days
# output: list of returns of the stock for n-1 days
def get_returns(prices):
    returns = []
    for day in range(len(prices) - 1):
        returns.append(np.log(prices[day + 1] / prices[day]))
    return returns

# input: correlations matrix of N random values and number of observations
# output: N random sequences (normal distribution) of length n
def get_norm_seq(matrix, n):
  return np.random.multivariate_normal(mean=np.zeros(len(matrix[0])), cov=matrix, size=n).T

# input: returns of one stock
# output: indicators of the returns of the stock
def get_indicators(returns):
  inds = []
  for ret in returns:
    if (ret > 0):
      inds.append(1)
    else:
      inds.append(0)
  return inds

# input: matrix of returns of N stocks for n days
# output: matrix of indicators of the returns of N stocks for n days
def get_inds_matrix(returns):
  ret_inds = []
  for stock in returns:
    ret_inds.append(get_indicators(stock))
  return ret_inds

## input: returns of two stocks
## output: sign coefficient of the stocks
# def get_sign_coef(stock_1, stock_2):
#   count = 0
#   for t in range(len(stock_1)):
#     if (stock_1[t] == stock_2[t]):
#       count += 1
#   return count

## input: matrix of indicators of stocks returns
## output: matrix of sign coefficients of NxN pair of stocks
# def get_coef_matrix(ret_inds):
#   sign_coef_matrix = []
#   for i in range(len(ret_inds)):
#     sign_coef_matrix.append([])
#     for j in range(len(ret_inds)):
#       sign_coef_matrix[i].append(get_sign_coef(ret_inds[i], ret_inds[j]))
#   return sign_coef_matrix

