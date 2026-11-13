def simplify(x, n):
    from fractions import Fraction
    
    x_frac = Fraction(x)
    n_frac = Fraction(n)
    
    result = x_frac * n_frac
    
    return result.denominator == 1