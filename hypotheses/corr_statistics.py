import numpy as np
from scipy.stats import norm

# def porog(alpha=0.05):
#     return norm.ppf(1 - alpha)
#
# def test_corr(corr, n_oserv, alpha):
#     N = len(corr)
#     stats = np.ones((N, N))
#     for i in range(N):
#         for j in range(N):
#             if i > j:
#                 a = (1 / 2) * np.log((1 + corr[i][j]) / (1 - corr[i][j]))
#                 b = -(1 / 2) * np.log((1 + porog(alpha)) / (1 - porog(alpha)))
#                 stats[i, j] = np.sqrt(n_oserv - 3) * (a + b)
#                 stats[j, i] = stats[i, j]
#
#
# def test_ijk(i, j, k, corr, n_oserv, alpha):
#     N = len(corr)
#     stat_ij = (1 / 2) * np.log((1 + corr[i][j]) / (1 - corr[i][j]))
#     stat_ik = (1 / 2) * np.log((1 + corr[i][k]) / (1 - corr[i][k]))
#     b = -(1 / 2) * np.log((1 + porog(alpha)) / (1 - porog(alpha)))
#
#     return (np.sqrt(n_oserv - 3) * (stat_ij + b)) > (np.sqrt(n_oserv - 3) * (stat_ik + b))
#
#
# def test_ijk(i, j, k, l, corr, n_oserv, alpha):
#     N = len(corr)
#     stat_ij = (1 / 2) * np.log((1 + corr[i][j]) / (1 - corr[i][j]))
#     stat_kl = (1 / 2) * np.log((1 + corr[k][l]) / (1 - corr[k][l]))
#     b = -(1 / 2) * np.log((1 + porog(alpha)) / (1 - porog(alpha)))
#
#     return (np.sqrt(n_oserv - 3) * (stat_ij + b)) > (np.sqrt(n_oserv - 3) * (stat_kl + b))
