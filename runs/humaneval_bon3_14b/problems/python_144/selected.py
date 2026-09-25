from fractions import Fraction

def simplify(x, n):
    # Convert the string representations of fractions to Fraction objects
    frac_x = Fraction(x)
    frac_n = Fraction(n)
    
    # Multiply the fractions
    result = frac_x * frac_n
    
    # Check if the result is a whole number
    return result.denominator == 1