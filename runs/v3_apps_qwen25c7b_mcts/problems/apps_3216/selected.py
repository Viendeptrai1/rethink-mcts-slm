from fractions import Fraction

def convert_repeating_decimal_to_fraction(decimal_str, repeat_len):
    # Split the decimal string into non-repeating and repeating parts
    non_repeat_part, repeat_part = decimal_str.split('.')
    repeat_part = repeat_part[:repeat_len]
    
    # Calculate the numerator and denominator
    num_non_repeat = int(non_repeat_part)
    num_repeat = int(repeat_part)
    denom_length = len(repeat_part)
    denom = int('9' * denom_length)
    
    # Combine the non-repeating and repeating parts into a single integer
    combined_num = num_non_repeat * (denom // 9) + num_repeat
    
    # Create a fraction and simplify it
    fraction = Fraction(combined_num, denom)
    
    return fraction

# Read input from stdin
input_line = input().strip()
decimal_str, repeat_len = input_line.split()
repeat_len = int(repeat_len)

# Convert the repeating decimal to a fraction and print the result
result = convert_repeating_decimal_to_fraction(decimal_str, repeat_len)
print(result)