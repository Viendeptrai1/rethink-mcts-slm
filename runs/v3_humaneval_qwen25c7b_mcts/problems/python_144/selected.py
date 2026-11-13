from fractions import Fraction

def simplify(x, n):
    return (Fraction(x) * Fraction(n)).denominator == 1