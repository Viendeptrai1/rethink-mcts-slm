import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return

    has_dot = '.' in s
    if has_dot:
        int_part, frac_part = s.split('.')
    else:
        int_part = s
        frac_part = ""

    # Remove leading zeros from integer part
    while len(int_part) > 1 and int_part[0] == '0':
        int_part = int_part[1:]

    # Remove trailing zeros from fractional part
    while frac_part and frac_part[-1] == '0':
        frac_part = frac_part[:-1]

    # Find the first non-zero digit
    idx = 0
    while idx < len(int_part) and int_part[idx] == '0':
        idx += 1

    if idx == len(int_part):
        # All integer part is zeros, look in fractional part
        if not frac_part:
            # Input was "0" or "00" etc., but problem says positive number
            # So this case shouldn't happen for positive x unless x=0 which is not positive
            # But if it does, handle as 0E0? Problem says positive, so assume at least one non-zero.
            # If frac_part is also empty or all zeros, it's 0, but input is positive.
            # Let's assume valid positive input.
            # If we reach here, it means number is 0, which contradicts "positive".
            # However, to be safe, if no non-zero found, output 0E0? 
            # But examples don't show 0. Let's assume there is a non-zero digit.
            # If frac_part exists and has non-zero:
            first_nonzero_idx = 0
            while first_nonzero_idx < len(frac_part) and frac_part[first_nonzero_idx] == '0':
                first_nonzero_idx += 1
            if first_nonzero_idx == len(frac_part):
                # Should not happen for positive number
                print("0E0")
                return
            idx = len(int_part) + first_nonzero_idx
        else:
            # All integer part zeros, first non-zero in frac
            idx = len(int_part) + 0 # We will adjust logic below
            # Actually, let's re-scan properly
            # Re-find first non-zero considering both parts
            combined = int_part + frac_part
            idx = 0
            while idx < len(combined) and combined[idx] == '0':
                idx += 1
            # Now idx is the index in the combined string (without dot)
            # But we need to know where the decimal point was relative to this.
            pass

    # Let's restart the index finding logic cleanly
    # We have int_part and frac_part. The original number is int_part . frac_part
    # We removed leading zeros from int_part and trailing from frac_part.
    # Now find the first non-zero digit in the normalized string.
    
    # Re-construct the sequence of digits without the dot
    digits = int_part + frac_part
    
    # Find first non-zero
    first_nonzero_pos = 0
    while first_nonzero_pos < len(digits) and digits[first_nonzero_pos] == '0':
        first_nonzero_pos += 1
    
    # If no non-zero found (shouldn't happen for positive x)
    if first_nonzero_pos == len(digits):
        print("0E0")
        return

    # Calculate exponent
    # The decimal point is after int_part (length of int_part)
    # The position of the first non-zero digit relative to the decimal point:
    # If the digit is at index i in the combined string (0-indexed from left),
    # and the decimal point is after index (len(int_part)-1), then:
    # The exponent b is such that the number is a * 10^b.
    # The first digit 'a' is at position first_nonzero_pos in the combined string.
    # The decimal point is effectively at position len(int_part) in the combined string (0 to len(int_part)-1 are integer digits).
    # So the number of digits before the first non-zero digit is first_nonzero_pos.
    # The decimal point is after len(int_part) digits? No.
    # Example: 123.45 -> int_part="123", frac_part="45", digits="12345"
    # Decimal point is after "123", so after index 2 (0-based).
    # First non-zero is at index 0.
    # Exponent = (position of decimal point) - (position of first non-zero)
    # Position of decimal point = len(int_part)
    # Exponent = len(int_part) - first_nonzero_pos
    
    # Example: .123 -> int_part="", frac_part="123", digits="123"
    # len(int_part)=0, first_nonzero_pos=0
    # Exponent = 0 - 0 = 0? But .123 = 1.23 * 10^-1.
    # Wait, the formula: 
    # x = d_k ... d_0 . d_{-1} ...
    # If we write x = a * 10^b, where a is in [1, 10).
    # a = d_k . d_{k-1} ... d_0 d_{-1} ... (shifted so first digit is before decimal)
    # The exponent b is the number of places we moved the decimal point to the left to get a.
    # Original decimal point position: after len(int_part) digits (if we consider the combined string).
    # New decimal point position: after the first digit (index 0).
    # Moves to left = (original position) - (new position)
    # Original position = len(int_part)
    # New position = 1 (since we put decimal after first digit, which is at index 0, so position 1)
    # b = len(int_part) - 1 - first_nonzero_pos? 
    # Let's test:
    # 123.45: int_part="123" (len=3), first_nonzero=0. 
    # We want 1.2345E2. b=2.
    # Formula: len(int_part) - 1 - first_nonzero_pos = 3 - 1 - 0 = 2. Correct.
    # .123: int_part="" (len=0), first_nonzero=0.
    # We want 1.23E-1. b=-1.
    # Formula: 0 - 1 - 0 = -1. Correct.
    # 0.00123: int_part="00" -> normalized to ""? No, we removed leading zeros.
    # Original: "0.00123" -> int_part="0", frac_part="00123"
    # Remove leading zeros from int_part: "0" -> ""? No, "0" has length 1, removing leading zeros leaves empty? 
    # My code: while len>1 and '0': remove. So "0" stays "0".
    # Then remove trailing zeros from frac: "00123" -> "123".
    # int_part="0", frac_part="123".
    # digits = "0123".
    # first_nonzero_pos = 1 (the '1').
    # len(int_part) = 1.
    # b = 1 - 1 - 1 = -1.
    # Result: 1.23E-1. Correct.
    # 100.: int_part="100", frac_part="" -> "100", "".
    # digits="100", first_nonzero=0.
    # b = 3 - 1 - 0 = 2.
    # Result: 1E2. Correct.
    # 01.23400: int_part="01" -> "1", frac_part="23400" -> "234".
    # digits="1234", first_nonzero=0.
    # len(int_part)=1.
    # b = 1 - 1 - 0 = 0.
    # Result: 1.234. Correct.
    
    b = len(int_part) - 1 - first_nonzero_pos

    # Construct mantissa
    # a = digits[first_nonzero_pos] + "." + digits[first_nonzero_pos+1:]
    # But we need to handle if there are no more digits after the first one.
    
    first_digit = digits[first_nonzero_pos]
    rest = digits[first_nonzero_pos+1:]
    
    if not rest:
        mantissa = first_digit
    else:
        mantissa = first_digit + "." + rest

    # Format output
    if b == 0:
        print(mantissa)
    else:
        print(f"{mantissa}E{b}")

if __name__ == "__main__":
    solve()