from fractions import Fraction

def find_rational_number(decimal_str, repeat_count):
    # Extract the non-repeating and repeating parts
    non_repeating, repeating = decimal_str.split('.')
    repeating = repeating[:repeat_count]
    
    # Create the numerator and denominator
    numerator = int(non_repeating + repeating)
    denominator = int('9' * repeat_count + '0' * len(non_repeating))
    
    # Simplify the fraction
    fraction = Fraction(numerator, denominator)
    
    return f"{fraction.numerator}/{fraction.denominator}"

# Example usage
if __name__ == "__main__":
    import sys
    input_line = sys.stdin.read().strip()
    decimal_str, repeat_count = input_line.split()
    repeat_count = int(repeat_count)
    result = find_rational_number(decimal_str, repeat_count)
    print(result)