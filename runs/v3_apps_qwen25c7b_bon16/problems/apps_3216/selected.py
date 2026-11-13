from fractions import Fraction
import sys

def find_fraction(decimal_str, repeat_len):
    non_repeating = int(decimal_str[:decimal_str.index('.')])
    decimal_part = decimal_str[decimal_str.index('.') + 1:]
    repeating_part = decimal_part[:repeat_len]
    non_repeating_part = decimal_part[repeat_len:]

    if non_repeating == 0:
        num = int(repeating_part)
    else:
        num = int(non_repeating * (10 ** len(non_repeating_part)) + int(repeating_part))

    den = int('9' * repeat_len + '0' * len(non_repeating_part))
    
    return str(Fraction(num, den).limit_denominator())

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    decimal_str, repeat_len = input_line.split()
    repeat_len = int(repeat_len)
    result = find_fraction(decimal_str, repeat_len)
    print(result)