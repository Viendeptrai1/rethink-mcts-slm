def find_fraction():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    decimal_str = data[0]
    repeating_length = int(data[1])
    
    # Remove the decimal point
    decimal_str = decimal_str.replace('.', '')
    
    # Determine the non-repeating and repeating parts
    non_repeating_length = len(decimal_str) - repeating_length
    non_repeating_part = decimal_str[:non_repeating_length]
    repeating_part = decimal_str[non_repeating_length:]
    
    # Convert the non-repeating part to an integer
    if non_repeating_part:
        non_repeating_int = int(non_repeating_part)
    else:
        non_repeating_int = 0
    
    # Convert the repeating part to an integer
    repeating_int = int(repeating_part)
    
    # Calculate the denominator
    denominator = 10**repeating_length - 1
    
    # Calculate the numerator
    numerator = repeating_int - non_repeating_int * (10**repeating_length)
    
    # Simplify the fraction
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    common_divisor = gcd(numerator, denominator)
    numerator //= common_divisor
    denominator //= common_divisor
    
    print(numerator, denominator)