def find_fraction(decimal_str, repeating_length):
    # Remove leading zeroes and decimal point
    if decimal_str.startswith('0.'):
        decimal_str = decimal_str[2:]
    
    non_repeating = decimal_str[:-repeating_length]
    repeating = decimal_str[-repeating_length:]

    # Calculate the numerator and denominator
    if non_repeating:
        non_repeating_decimal_value = int(non_repeating)
    else:
        non_repeating_decimal_value = 0

    multiplier = 10 ** len(non_repeating)
    numerator = non_repeating_decimal_value * multiplier + int(repeating) - non_repeating_decimal_value

    # The denominator will be based on the repeating part
    denominator = int('9' * len(repeating) + '0' * len(non_repeating))

    # Reducing the fraction by computing gcd
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    common_divisor = gcd(numerator, denominator)
    numerator //= common_divisor
    denominator //= common_divisor

    print(f"{numerator}/{denominator}")

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    find_fraction(data[0], int(data[1]))