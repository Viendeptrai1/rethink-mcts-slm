import sys
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    line = sys.stdin.readline().strip()
    if not line:
        return
    
    parts = line.split()
    decimal_str = parts[0]
    repeat_count = int(parts[1])
    
    dot_index = decimal_str.find('.')
    integer_part = decimal_str[:dot_index]
    decimal_part = decimal_str[dot_index+1:]
    
    non_repeat_len = len(decimal_part) - repeat_count
    repeat_part = decimal_part[non_repeat_len:]
    non_repeat_part = decimal_part[:non_repeat_len]
    
    # Form the numerator: (all_digits - non_repeating_digits)
    # all_digits = integer_part + non_repeat_part + repeat_part
    # non_repeating_digits = integer_part + non_repeat_part
    
    all_digits_str = integer_part + non_repeat_part + repeat_part
    non_repeat_digits_str = integer_part + non_repeat_part
    
    num_all = int(all_digits_str) if all_digits_str else 0
    num_non = int(non_repeat_digits_str) if non_repeat_digits_str else 0
    
    numerator = num_all - num_non
    
    # Form the denominator:
    # repeat_count 9s followed by non_repeat_len 0s
    denom_str = '9' * repeat_count + '0' * non_repeat_len
    denominator = int(denom_str) if denom_str else 1
    
    common = gcd(numerator, denominator)
    numerator //= common
    denominator //= common
    
    print(f"{numerator}/{denominator}")

if __name__ == "__main__":
    solve()