from fractions import Fraction

def repeating_decimal_to_fraction(decimal_str, repeat_length):
    # Split the decimal string into non-repeating and repeating parts
    non_repeating, repeating = decimal_str.split('.')
    
    # Convert non-repeating part to a fraction
    if non_repeating == '0':
        non_repeating_fraction = Fraction(0)
    else:
        non_repeating_fraction = Fraction(int(non_repeating))
    
    # Convert repeating part to a fraction
    repeating_digits = repeating[-repeat_length:]
    repeating_fraction = Fraction(int(repeating_digits), int('9' * repeat_length))
    
    # Combine the two fractions
    total_fraction = non_repeating_fraction + repeating_fraction
    
    # Simplify the fraction
    total_fraction = total_fraction.limit_denominator()
    
    return total_fraction.numerator, total_fraction.denominator

# Read input from stdin
import sys
input_line = sys.stdin.read().strip()
decimal_str, repeat_length = input_line.split()
repeat_length = int(repeat_length)

# Get the fraction
numerator, denominator = repeating_decimal_to_fraction(decimal_str, repeat_length)

# Print the result
print(f"{numerator}/{denominator}")