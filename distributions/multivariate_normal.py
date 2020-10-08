import numpy as np


def norm_seq(sigma, n, mu=None):
    """
    Produce n samples of N-dimensional multivariate normal distribution

    Args:
        mu (numpy.ndarray): mean vector
        sigma (numpy.ndarray): scale matrix NxN (covariance)
        n (int): # of samples to produce

    Returns:
        numpy.ndarray
    """
    if not mu:
        mu = np.zeros(len(sigma))
    return np.random.multivariate_normal(mu, sigma, n).T
