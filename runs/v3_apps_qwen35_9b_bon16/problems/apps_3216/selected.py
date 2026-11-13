import sys
import math
from fractions import Fraction

def solve():
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return
        
        parts = input_data.split()
        decimal_str = parts[0]
        repeat_count = int(parts[1])
        
        # Split integer and fractional parts
        int_part, frac_part = decimal_str.split('.')
        
        n_digits = len(frac_part)
        
        # Define the repeating part and non-repeating part of the fraction
        # The number is: int_part . (non_repeating_part)(repeating_part)
        # where repeating_part has length = repeat_count
        
        repeating_part = frac_part[-repeat_count:]
        non_repeating_part = frac_part[:-repeat_count] if repeat_count < n_digits else ""
        
        # Construct the numerator and denominator based on the formula for repeating decimals:
        # Number = A . B(over C)
        # Where:
        # A = integer part
        # B = non-repeating fractional digits
        # C = repeating fractional digits
        
        # Formula:
        # Value = (Integer formed by all digits except the decimal point) 
        #        - (Integer formed by integer part + non-repeating part)
        #        ----------------------------------------------------
        #        (9...9) [repeat_count times] * (10...0) [length of non-repeating part times] + (10...0) [repeat_count times]
        
        # Let's build the numbers carefully using integers.
        
        # Let N be the number formed by the entire string of digits (integer part + fractional part)
        # But we need to handle the decimal point logic precisely.
        
        # Let's use the standard algebraic method:
        # Let x = integer_part + fraction
        # x = I + 0.b1b2...bk(c1c2...cn) where k = len(non_repeating), n = len(repeating)
        
        # To avoid float precision issues, we work with integers directly.
        
        # Let P be the integer formed by the entire sequence of digits after the decimal point (non-repeating + repeating)
        # Let Q be the integer formed by the non-repeating part only (if any)
        # Let R be the integer formed by the integer part
        
        # Actually, simpler approach:
        # The number is: R + (Q * 10^-k + (P - Q) * 10^-k * 10^-n * (1 / (10^n - 1)))? No, that's getting messy.
        
        # Standard Formula for 0.ABCDE(FGH) where ABCDE is non-repeating (len k) and FGH is repeating (len n):
        # Value = (Integer(ABCDEFGH) - Integer(ABCDE)) / (Integer(n nines) * Integer(k zeros) + Integer(n nines))
        # Wait, the integer part R is also there.
        
        # Full Number = R + FractionPart
        # FractionPart = (Integer(NonRepeatingRepeating) - Integer(NonRepeating)) / ( (10^n - 1) * 10^k )
        # Where:
        # NonRepeatingRepeating = integer formed by concatenating non-repeating part and repeating part
        # NonRepeating = integer formed by non-repeating part
        # n = length of repeating part
        # k = length of non-repeating part
        
        # So Total = R + (Num_Frac / Den_Frac)
        # Total = (R * Den_Frac + Num_Frac) / Den_Frac
        
        if len(frac_part) == 0:
            # No fractional part, just an integer
            num = int(int_part)
            den = 1
        else:
            n = repeat_count
            k = len(frac_part) - n
            
            # Non-repeating part digits
            if k > 0:
                non_rep_str = frac_part[:k]
                non_rep_int = int(non_rep_str) if non_rep_str else 0
            else:
                non_rep_int = 0
            
            # Full fractional digits string (non-repeating + repeating)
            full_frac_str = frac_part
            full_frac_int = int(full_frac_str) if full_frac_str else 0
            
            # Denominator construction:
            # (10^n - 1) * 10^k
            denom_factor1 = 10**n - 1  # n nines
            denom_factor2 = 10**k       # k zeros
            denominator = denom_factor1 * denom_factor2
            
            # Numerator construction for the fractional part only:
            # full_frac_int - non_rep_int
            frac_numerator = full_frac_int - non_rep_int
            
            # Now add the integer part R
            if int_part:
                int_val = int(int_part)
                # Total Numerator = int_val * denominator + frac_numerator
                numerator = int_val * denominator + frac_numerator
            else:
                numerator = frac_numerator
            
        result = Fraction(numerator, denominator)
        print(f"{result.numerator}/{result.denominator}")

    except Exception:
        pass

if __name__ == "__main__":
    solve()