
"""Statistics T2, T3 for hypothesis H_i,j,k"""
# input: matrix of returns of stocks and indexes of 3 stocks
# output: statistic
def stat_T2(ret_inds, i, j, k):
  _sum = 0
  for t in range(len(ret_inds[0])):
    _sum += (ret_inds[i][t] * ret_inds[j][t] * (1 - ret_inds[k][t])) + \
            ((1 - ret_inds[i][t]) * (1 - ret_inds[j][t]) * ret_inds[k][t])
  return _sum

def stat_T3(ret_inds, i, j, k):
  _sum = 0
  for t in range(len(ret_inds[0])):
    _sum += (ret_inds[i][t] * (1 - ret_inds[j][t]) * ret_inds[k][t]) + \
            ((1 - ret_inds[i][t]) * ret_inds[j][t] * (1 - ret_inds[k][t]))
  return _sum

"""Statistics R2, R3 for hypothesis H_i,j,k,l"""
# input: matrix of returns of stocks and indexes of 4 stocks
# output: statistic
def stat_R2(ret_inds, i, j, k, l):
  _sum = 0
  for t in range(len(ret_inds[0])):
    if ret_inds[i][t] == ret_inds[j][t] and ret_inds[k][t] != ret_inds[l][t]:
      _sum += 1
  return _sum


def stat_R3(ret_inds, i, j, k, l):
  _sum = 0
  for t in range(len(ret_inds[0])):
    if ret_inds[i][t] != ret_inds[j][t] and ret_inds[k][t] == ret_inds[l][t]:
      _sum += 1
  return _sum