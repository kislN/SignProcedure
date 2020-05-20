import numpy as np
from scipy.stats import norm

# def threshold_c(alpha=0.05):
#     return norm.ppf(1 - alpha)
#
# def test_corr(corr, n_observ, alpha):
#     N = len(corr)
#     stats = np.ones((N, N))
#     for i in range(N):
#         for j in range(N):
#             if i > j:
#                 a = (1 / 2) * np.log((1 + corr[i][j]) / (1 - corr[i][j]))
#                 b = -(1 / 2) * np.log((1 + threshold) / (1 - threshold))
#                 stats[i, j] = np.sqrt(n_observ - 3) * (a + b)
#                 stats[j, i] = stats[i, j]

