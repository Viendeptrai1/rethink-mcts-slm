import math
import cmath

def find_zero(xs: list):
    def poly(x):
        return sum(coeff * math.pow(x, i) for i, coeff in enumerate(xs))

    def derivative(x):
        return sum(i * coeff * math.pow(x, i - 1) for i, coeff in enumerate(xs) if i > 0)
    
    def newton_raphson(initial_guess=0.0, tolerance=1e-7, max_iterations=1000):
        x = initial_guess
        for _ in range(max_iterations):
            poly_x = poly(x)
            if abs(poly_x) < tolerance:
                return x
            deriv_x = derivative(x)
            if deriv_x == 0:
                return x
            x = x - poly_x / deriv_x
        return x

    return newton_raphson()