import numpy as np

def fit_projectile(coords):
    """
    Fits real projectile motion:
    x(t) = ax t^2 + bx t + c (optional)
    y(t) = ay t^2 + by t + c
    """

    if len(coords) < 5:
        raise ValueError("Not enough points for physics fit")

    x = np.array([p[0] for p in coords])
    y = np.array([p[1] for p in coords])
    t = np.arange(len(coords))

    # quadratic fit (gravity shows up here in y)
    x_coeffs = np.polyfit(t, x, 2)
    y_coeffs = np.polyfit(t, y, 2)

    x_curve = np.poly1d(x_coeffs)
    y_curve = np.poly1d(y_coeffs)

    return t, x_curve, y_curve

def estimate_gravity(y_curve):
    """
    Estimates gravity-like acceleration from fitted y(t) curve.
    y = a t^2 + b t + c
    g ≈ 2a (sign depends on coordinate system)
    """

    a = y_curve.c[0]   # coefficient of t^2

    g_est = 2 * a

    return g_est
