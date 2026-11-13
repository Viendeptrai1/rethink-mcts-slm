import math

def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

def poly_derivative(xs: list, x: float):
    """
    Evaluates the derivative of the polynomial with coefficients xs at point x.
    """
    return sum([i * coeff * math.pow(x, i - 1) for i, coeff in enumerate(xs) if i > 0])

def find_zero(xs: list):
    """ xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only one zero point, even if there are many.
    Moreover, find_zero only takes list xs having an even number of coefficients
    and largest non-zero coefficient as it guarantees
    a solution.
    """
    # Initial guesses for the bisection method
    a, b = -1000, 1000
    tolerance = 1e-7
    max_iterations = 1000

    for _ in range(max_iterations):
        fa = poly(xs, a)
        fb = poly(xs, b)

        if abs(fa) < tolerance:
            return a
        if abs(fb) < tolerance:
            return b

        if fa * fb >= 0:
            raise ValueError("The function has the same sign at the endpoints a and b.")

        # Midpoint
        c = (a + b) / 2
        fc = poly(xs, c)

        if abs(fc) < tolerance:
            return c

        if fa * fc < 0:
            b = c
        else:
            a = c

    raise ValueError("Bisection method did not converge")