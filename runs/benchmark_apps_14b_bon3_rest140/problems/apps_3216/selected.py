from fractions import Fraction

def find_fraction(decimal_str, repeat_length):
    # Split the input string into the non-repeating and repeating parts
    non_repeating, repeating = decimal_str.split('.')
    
    # Calculate the length of the non-repeating part
    non_repeat_length = len(non_repeating)
    
    # Create the full repeating decimal as a string
    full_repeating = repeating + repeating[:repeat_length]
    
    # Convert the full repeating decimal to a fraction
    numerator = int(full_repeating)
    denominator = 10 ** len(full_repeating) - 1
    
    # Adjust for the non-repeating part
    if non_repeat_length > 0:
        non_repeating_part = int(non_repeating) * (10 ** repeat_length)
        repeating_part = int(repeating[:repeat_length])
        numerator = non_repeating_part + repeating_part
        denominator = (10 ** non_repeat_length) * (10 ** repeat_length - 1)
    
    # Reduce the fraction to its simplest form
    fraction = Fraction(numerator, denominator)
    
    # Return the result as a string
    return f"{fraction.numerator}/{fraction.denominator}"

# Read input from standard input
import sys
input_data = sys.stdin.read().strip()
decimal_str, repeat_length = input_data.split()

# Convert repeat_length to an integer
repeat_length = int(repeat_length)

# Find and print the fraction
print(find_fraction(decimal_str, repeat_length))