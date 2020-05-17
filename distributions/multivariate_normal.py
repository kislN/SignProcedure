import numpy as np

# input: correlations matrix of N random values and number of observations
# output: N random sequences (normal distribution) of length n
def get_norm_seq(cov, n):
  return np.random.multivariate_normal(mean=np.zeros(len(cov)), cov=cov, size=n).T