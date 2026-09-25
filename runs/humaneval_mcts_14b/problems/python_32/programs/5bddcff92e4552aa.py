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
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    """
    if len(xs) % 2 != 0 or not any(xs):
        raise ValueError("The input list must have an even number of coefficients and at least one non-zero coefficient.")
    
    # Initial guess for the root
    x0 = 0.0
    
    # Tolerance and maximum number of iterations
    tolerance = 1e-7
    max_iterations = 1000
    
    for _ in range(max_iterations):
        fx = poly(xs, x0)
        fpx = poly_derivative(xs, x0)
        
        if abs(fpx) < tolerance:
            raise ValueError("Derivative near zero, no convergence possible.")
        
        x1 = x0 - fx / fpx
        
        if abs(x1 - x0) < tolerance:
            return x1
        
        x0 = x1
    
    raise ValueError("Maximum iterations reached, no convergence.")

# Example usage
print(round(find_zero([1, 2]), 2))  # f(x) = 1 + 2x
print(round(find_zero([-6, 11, -6, 1]), 2))  # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3