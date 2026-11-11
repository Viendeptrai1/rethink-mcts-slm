from fractions import Fraction

def find_fraction(decimal_str, repeat_length):
    # Split the input string into the non-repeating and repeating parts
    non_repeating, repeating = decimal_str.split('.')
    
    # Convert the non-repeating and repeating parts to integers
    non_repeating = int(non_repeating)
    repeating = int(repeating)
    
    # Calculate the length of the non-repeating part
    non_repeat_length = len(str(non_repeating))
    
    # Create the fraction representation
    if non_repeat_length == 0:
        # If there's no non-repeating part, it's just a repeating decimal
        numerator = repeating
        denominator = 10**repeat_length - 1
    else:
        # If there's a non-repeating part, handle it separately
        numerator = non_repeating * (10**repeat_length - 1) + repeating
        denominator = 10**(non_repeat_length + repeat_length) - 10**non_repeat_length
    
    # Use the Fraction class to reduce the fraction to its simplest form
    fraction = Fraction(numerator, denominator)
    
    # Return the fraction as a string in the format "numerator/denominator"
    return f"{fraction.numerator}/{fraction.denominator}"

# Read input from standard input
import sys
input_line = sys.stdin.read().strip()

# Parse the input
decimal_str, repeat_length = input_line.split()
repeat_length = int(repeat_length)

# Find and print the fraction
print(find_fraction(decimal_str, repeat_length))