import math

def poly(xs: list, x: float):
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

def derivative(xs: list, x: float):
    return sum([i * coeff * math.pow(x, i-1) for i, coeff in enumerate(xs) if i > 0])

def find_zero(xs: list):
    if len(xs) % 2 != 0 or xs[-1] == 0:
        raise ValueError("List must have an even number of coefficients and the largest non-zero coefficient must be present.")
    
    x = 0.0
    while True:
        fx = poly(xs, x)
        dfx = derivative(xs, x)
        if abs(fx) < 1e-9:
            return round(x, 2)
        x -= fx / dfx