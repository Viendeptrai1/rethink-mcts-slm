import math
from scipy.optimize import bisect

def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

def find_zero(xs: list):
    """ xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only one zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    """
    assert len(xs) % 2 == 0, "The number of coefficients must be even."
    
    # Define the polynomial function using the coefficients
    def f(x):
        return poly(xs, x)
    
    # Use the bisection method to find a root
    # We need to find an interval [a, b] where f(a) and f(b) have opposite signs
    a, b = -1000, 1000  # Initial interval, can be adjusted
    while f(a) * f(b) > 0:
        a *= 2
        b *= 2
    
    # Use bisect to find the root within the interval
    return bisect(f, a, b)

# Example usage
print(round(find_zero([1, 2]), 2))  # f(x) = 1 + 2x
print(round(find_zero([-6, 11, -6, 1]), 2))  # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3