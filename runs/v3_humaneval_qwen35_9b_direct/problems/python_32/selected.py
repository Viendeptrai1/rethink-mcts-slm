import math

def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

def find_zero(xs: list):
    """
    xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only only zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    """
    low = -1.0
    high = 1.0
    
    # Expand the search range until we find an interval where the sign changes
    while poly(xs, low) * poly(xs, high) > 0:
        low *= 2
        high *= 2
    
    # Binary search for the root
    for _ in range(100):
        mid = (low + high) / 2
        if poly(xs, mid) == 0:
            return mid
        if poly(xs, low) * poly(xs, mid) < 0:
            high = mid
        else:
            low = mid
            
    return (low + high) / 2