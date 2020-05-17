import numpy as np

def get_Student_seq(cov, dof, n):
    """
    Produce m samples of d-dimensional multivariate t distribution

    Args:
        mu (numpy.ndarray): mean vector
        sigma (numpy.ndarray): scale matrix (covariance)
        dof (float): degrees of freedom
        m (int): # of samples to produce

    Returns:
        numpy.ndarray
    """
    mu = np.zeros(len(cov))
    g = np.tile(np.random.gamma(dof / 2, 2 / dof, n), (len(cov), 1)).T
    z = np.random.multivariate_normal(mu, cov, n)
    return (mu + z / np.sqrt(g)).T