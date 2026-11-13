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
    fractional_part = decimal_str[dot_index+1:]
    
    non_repeating_len = len(fractional_part) - repeat_count
    repeating_part = fractional_part[non_repeating_len:]
    non_repeating_part = fractional_part[:non_repeating_len]
    
    # Convert to fraction: value = integer_part + (non_repeating_part + repeating_part) / 10^len(fractional_part)
    # But we need to handle the repeating part algebraically.
    # Let x = 0.non_repeating_part_repeating_part...
    # x = (non_repeating_part as integer) / 10^non_repeating_len + (repeating_part as integer) / (10^non_repeating_len * (10^repeat_count - 1))
    
    int_val = int(integer_part) if integer_part else 0
    
    if non_repeating_len == 0:
        # Purely repeating: 0.repeating_part
        num_rep = int(repeating_part) if repeating_part else 0
        den_rep = 10**repeat_count - 1
        frac_val = num_rep / den_rep
    else:
        # Mixed repeating
        num_non_rep = int(non_repeating_part) if non_repeating_part else 0
        num_rep = int(repeating_part) if repeating_part else 0
        
        # Value = num_non_rep / 10^non_repeating_len + num_rep / (10^non_repeating_len * (10^repeat_count - 1))
        # Common denominator = 10^non_repeating_len * (10^repeat_count - 1)
        den_common = (10 ** non_repeating_len) * (10 ** repeat_count - 1)
        num_common = num_non_rep * (10 ** repeat_count - 1) + num_rep * (10 ** non_repeating_len)
        
        frac_val = num_common / den_common
    
    total_val = int_val + frac_val
    
    # Convert total_val to fraction
    # total_val = A / B
    # We can compute numerator and denominator directly from the decimal representation logic
    # Alternatively, use fractions module logic manually to avoid float precision issues
    
    # Let's reconstruct the fraction from the string parts directly to avoid any float issues
    # Total number = integer_part . non_repeating_part repeating_part (repeating)
    # Let N = integer_part concatenated with non_repeating_part concatenated with repeating_part
    # Let M = integer_part concatenated with non_repeating_part
    # Let L = len(non_repeating_part)
    # Let R = len(repeating_part)
    # Value = (N - M) / (10^L * (10^R - 1))
    
    if non_repeating_len == 0:
        M_str = "0"
    else:
        M_str = integer_part + non_repeating_part
    
    N_str = integer_part + non_repeating_part + repeating_part
    
    M = int(M_str)
    N = int(N_str)
    
    L = non_repeating_len
    R = repeat_count
    
    denominator = (10 ** L) * (10 ** R - 1)
    numerator = N - M
    
    # Reduce fraction
    common = gcd(numerator, denominator)
    numerator //= common
    denominator //= common
    
    print(f"{numerator}/{denominator}")

if __name__ == "__main__":
    solve()