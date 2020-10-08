import numpy as np
from statsmodels.sandbox.distributions.multivariate import multivariate_t_rvs as gen_t


def student_seq(sigma, dof, n, mu=None):
    """
    Produce n samples of N-dimensional multivariate t distribution

    Args:
        mu (numpy.ndarray): mean vector
        sigma (numpy.ndarray): scale matrix NxN (covariance)
        dof (float): degrees of freedom
        n (int): # of samples to produce

    Returns:
        numpy.ndarray
    """
    if not mu:
        mu = np.zeros(len(sigma))
    g = np.tile(np.random.gamma(dof / 2, 2 / dof, n), (len(sigma), 1)).T
    z = np.random.multivariate_normal(mu, sigma, n)
    return (mu + z / np.sqrt(g)).T


def t_seq(sigma, dof, n, mu=None):
    """
    Produce n samples of N-dimensional multivariate t distribution

    Args:
        mu (numpy.ndarray): mean vector
        sigma (numpy.ndarray): scale matrix NxN (covariance)
        dof (float): degrees of freedom
        n (int): # of samples to produce

    Returns:
        numpy.ndarray
    """
    if not mu:
        mu = np.zeros(len(sigma))
    return gen_t(mu, sigma, dof, n).T
