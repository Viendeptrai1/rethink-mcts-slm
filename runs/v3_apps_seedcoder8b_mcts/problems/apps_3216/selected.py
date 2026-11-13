def find_fraction_from_repeating_decimal(decimal_str, repeat_count):
    # Split the input into the non-repeating and repeating parts
    non_repeating, repeating = decimal_str.split('.')
    
    # Remove leading zeros from the non-repeating part
    non_repeating = non_repeating.lstrip('0')
    
    # If there's no non-repeating part, start from the beginning of the repeating part
    if non_repeating == '':
        non_repeating = '0'
    
    # Calculate the integer part of the fraction
    integer_part = int(non_repeating)
    
    # Calculate the numerator and denominator of the repeating part
    repeating_part = repeating[:repeat_count]
    non_repeating_part = repeating[repeat_count:]
    
    # Calculate the numerator and denominator for the repeating part
    if non_repeating_part:
        numerator_repeating = int(repeating_part) - int(non_repeating_part)
        denominator_repeating = int('9' * repeat_count) - int('9' * len(non_repeating_part))
    else:
        numerator_repeating = int(repeating_part)
        denominator_repeating = int('9' * repeat_count)
    
    # Calculate the total numerator and denominator
    total_numerator = numerator_repeating + int(non_repeating) * denominator_repeating
    total_denominator = denominator_repeating
    
    # Calculate the gcd to reduce the fraction
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    common_divisor = gcd(total_numerator, total_denominator)
    reduced_numerator = total_numerator // common_divisor
    reduced_denominator = total_denominator // common_divisor
    
    return f"{reduced_numerator}/{reduced_denominator}"

# Read input
import sys
input = sys.stdin.read
data = input().strip().split()
decimal_str = data[0]
repeat_count = int(data[1])

# Get the result and print it
result = find_fraction_from_repeating_decimal(decimal_str, repeat_count)
print(result)