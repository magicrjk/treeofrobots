import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import sqrtm

from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import matplotlib.patches as patches

def hex_to_rgb(hex_string):
    r_hex = str(hex_string[1:3])
    g_hex = str(hex_string[3:5])
    b_hex = str(hex_string[5:7])
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)

def interpolate_color(t):
    """
    Linearly interpolate between green, blue, and red.

    :param t: A float between 0 and 1 representing the interpolation factor.
    :return: A string representing the interpolated color in hex format #RRGGBB.
    """
    # Ensure t is within the range [0, 1]
    t = max(0, min(1, t))
    
    if t < 0.5:
        # Interpolate between green and blue
        t = t * 2  # Scale t to the range [0, 1]
        r = 0
        g = int((1 - t) * 255)
        b = int(t * 255)
    else:
        # Interpolate between blue and red
        t = (t - 0.5) * 2  # Scale t to the range [0, 1]
        r = int(t * 255)
        g = 0
        b = int((1 - t) * 255)

    return f"#{r:02x}{g:02x}{b:02x}"

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The Axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)