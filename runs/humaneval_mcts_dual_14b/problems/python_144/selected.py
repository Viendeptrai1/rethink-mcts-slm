from fractions import Fraction

def simplify(x, n):
    # Convert the string fractions to Fraction objects
    frac_x = Fraction(x)
    frac_n = Fraction(n)
    
    # Calculate the product of the two fractions
    product = frac_x * frac_n
    
    # Check if the product is a whole number
    return product.denominator == 1