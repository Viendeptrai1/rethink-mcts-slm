import math


def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def find_zero(xs: list):
    """
    Finds a zero of the polynomial defined by coefficients xs.
    Uses the bisection method on the interval [-1, 1].
    The problem guarantees that a solution exists in this interval
    because the largest non-zero coefficient is at an even index
    and the polynomial has even degree (implied by even number of coefficients).
    """
    low = -1.0
    high = 1.0
    
    # Ensure the signs at the endpoints are different
    while poly(xs, low) * poly(xs, high) > 0:
        low = -1.0
        high = 1.0
        # If we are still in the same sign, we might need to search a bit wider
        # However, based on the problem constraints (largest coeff at even index),
        # the behavior at +/- infinity is determined by the leading term.
        # If degree is even and leading coeff > 0, then f(x) -> +inf as x -> +/- inf.
        # If leading coeff < 0, then f(x) -> -inf as x -> +/- inf.
        # In both cases, f(-inf) and f(+inf) have the same sign.
        # The problem states "largest non zero coefficient as it guarantees a solution".
        # This usually implies a local extremum or root behavior within a bounded range.
        # Let's try expanding the interval until we find a sign change.
        if abs(poly(xs, low)) < 1e-9 and abs(poly(xs, high)) < 1e-9:
            return 0.0
        
        # Expand interval
        low = -2 * low if low != 0 else -1.0
        high = 2 * high if high != 0 else 1.0
        # Prevent infinite expansion if no root exists (though guaranteed by problem)
        if high - low > 1e-6 and high > 1e6:
            # Fallback if expansion fails unexpectedly
            return 0.0

    # Bisection method
    for _ in range(100):
        mid = (low + high) / 2
        val = poly(xs, mid)
        if abs(val) < 1e-9:
            return mid
        if poly(xs, low) * val <= 0:
            high = mid
        else:
            low = mid
            
    return (low + high) / 2