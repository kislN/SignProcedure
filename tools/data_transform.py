import numpy as np


# input: list of prices of one stock for n days
# output: list of returns of the stock for n-1 days
def get_returns(prices):
    returns = []
    for day in range(len(prices) - 1):
        returns.append(np.log(prices[day + 1] / prices[day]))

    # return np.diff(np.log(np.array(prices)))
    return returns


# input: returns of one stock
# output: indicators of the returns of the stock
# def get_indicators(returns):
#     inds = []
#     for ret in returns:
#         if ret > 0:
#             inds.append(1)
#         else:
#             inds.append(0)
#     return inds


# input: matrix of returns of N stocks for n days
# output: matrix of indicators of the returns of N stocks for n days
def indicators(returns):
    return np.heaviside(returns, 0).astype(int)


# input: returns of two stocks
# output: sign coefficient of the stocks
def sign_coef(ind_i, ind_j):
    count = 0
    for t in range(len(ind_i)):
        if ind_i[t] == ind_j[t]:
            count += 1
    return count


# input: matrix of indicators of stocks returns
# output: matrix of sign coefficients of NxN pair of stocks
def get_sign_matrix(ret_inds):
    sign_matrix = []
    for i in range(len(ret_inds)):
        sign_matrix.append([])
        for j in range(len(ret_inds)):
            sign_matrix[i].append(sign_coef(ret_inds[i], ret_inds[j]))
    return sign_matrix

