import math

def poly(xs: list, x: float):
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

def find_zero(xs: list):
    def evaluate(coefficients, value):
        return poly(coefficients, value)
    
    def derivative(coefficients, value):
        return sum([i * coefficients[i] * math.pow(value, i-1) for i in range(1, len(coefficients))])
    
    def newton_raphson(coefficients, initial_guess, tolerance=1e-7, max_iterations=1000):
        x = initial_guess
        for _ in range(max_iterations):
            fx = evaluate(coefficients, x)
            dfx = derivative(coefficients, x)
            if abs(dfx) < tolerance:
                raise ValueError("Derivative too small; no convergence possible.")
            x_new = x - fx / dfx
            if abs(x_new - x) < tolerance:
                return x_new
            x = x_new
        raise ValueError("Maximum iterations reached; no convergence.")
    
    if len(xs) % 2 != 0:
        raise ValueError("List must have an even number of coefficients.")
    
    if xs[-1] == 0:
        raise ValueError("Largest non-zero coefficient must be present.")
    
    initial_guess = 0.0
    return newton_raphson(xs, initial_guess)