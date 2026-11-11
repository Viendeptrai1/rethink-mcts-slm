from fractions import Fraction

def repeating_decimal_to_fraction(decimal_str, repeat_length):
    # Split the decimal string into non-repeating and repeating parts
    non_repeating, repeating = decimal_str.split('.')
    
    # Convert the non-repeating and repeating parts to integers
    non_repeating_int = int(non_repeating)
    repeating_int = int(repeating)
    
    # Calculate the total number of digits after the decimal point
    total_digits = len(repeating)
    
    # Create the fraction using the formula for repeating decimals
    numerator = non_repeating_int * (10**total_digits - 10**(total_digits - repeat_length)) + repeating_int
    denominator = 10**total_digits - 10**(total_digits - repeat_length)
    
    # Reduce the fraction to its simplest form
    fraction = Fraction(numerator, denominator)
    
    # Return the fraction as a string in the format "numerator/denominator"
    return f"{fraction.numerator}/{fraction.denominator}"

# Read input from standard input
import sys
input_line = sys.stdin.read().strip()

# Parse the input
decimal_str, repeat_length_str = input_line.split()
repeat_length = int(repeat_length_str)

# Convert the repeating decimal to a fraction and print the result
result = repeating_decimal_to_fraction(decimal_str, repeat_length)
print(result)