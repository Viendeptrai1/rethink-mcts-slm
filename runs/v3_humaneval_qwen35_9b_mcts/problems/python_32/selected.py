import math

def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

def find_zero(xs: list):
    """
    Finds a zero of the polynomial defined by coefficients xs using the bisection method.
    Assumes the polynomial has at least one real root and that the largest coefficient
    ensures a sign change within a reasonable interval.
    """
    # Determine a safe interval [a, b] where the polynomial changes sign.
    # We start with a small range and expand until we find a sign change.
    a = -1.0
    b = 1.0
    
    # Expand the interval until we find a sign change or the values become too large
    while poly(xs, a) * poly(xs, b) > 0:
        a *= 2
        b *= 2
        if abs(a) > 1e12 or abs(b) > 1e12:
            # Fallback if expansion fails (though problem guarantees a solution)
            break

    # Bisection method
    for _ in range(100):  # Sufficient iterations for high precision
        c = (a + b) / 2
        if poly(xs, c) == 0:
            return c
        if poly(xs, a) * poly(xs, c) < 0:
            b = c
        else:
            a = c
            
    return (a + b) / 2