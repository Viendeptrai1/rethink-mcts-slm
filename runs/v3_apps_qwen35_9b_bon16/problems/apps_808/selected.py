import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return

    has_leading_dot = s.startswith('.')
    has_trailing_dot = s.endswith('.')
    has_explicit_dot = '.' in s

    # Determine if there is an integer part before the dot
    if has_leading_dot:
        int_part = "0"
        # Remove leading dot
        s = s[1:]
        # Check if the original was just "." or ".123"
        # If original was ".", s is empty now
        if not s:
            # Input was "." -> undefined for positive number? Assume 0? But problem says positive.
            # Let's assume valid input like .123
            pass
    else:
        # Find the position of the dot
        dot_idx = s.find('.')
        if dot_idx != -1:
            int_part = s[:dot_idx]
            s = s[dot_idx+1:]
        else:
            int_part = s
            s = ""

    # Clean up int_part: remove leading zeros, but keep at least one digit
    int_part = int_part.lstrip('0')
    if not int_part:
        int_part = "0"

    # Clean up fractional part: remove trailing zeros
    # If s is empty or all zeros, fractional part is effectively 0
    if s:
        # Remove trailing zeros
        s = s.rstrip('0')
        if not s:
            s = ""
    else:
        s = ""

    # Now we have int_part (non-empty, no leading zeros unless "0")
    # and s (fractional part without trailing zeros, possibly empty)
    # We need to form a number between 1 and 10.
    
    # Case 1: int_part is "0" (e.g., input ".123")
    if int_part == "0":
        # Number is 0.something
        # We need to move decimal to after first non-zero digit in s
        # Find first non-zero digit in s
        start_idx = 0
        while start_idx < len(s) and s[start_idx] == '0':
            start_idx += 1
        
        if start_idx == len(s):
            # Number is 0.000... -> but problem says positive, so this shouldn't happen with valid input
            # However, if input was .000, it's 0. But let's assume positive implies non-zero.
            # If it were 0, output would be 0E0? But spec says 1<=a<10.
            # Let's assume there is a non-zero digit.
            a = "0"
            b = 0
        else:
            a = s[start_idx] + "." + s[start_idx+1:]
            # Count how many zeros were skipped + 1 for the digit itself relative to the dot
            # Original decimal was at index -1 relative to string s (which is after the dot)
            # In the original string, the dot was before int_part (empty) and s.
            # The number of positions to move the decimal point to the right to get 'a'
            # is start_idx + 1.
            # Wait, let's trace: .00123 -> s="00123", start_idx=2 (digit '1')
            # We want 1.23. Original was 1.23 * 10^-3? No.
            # .00123 = 1.23 * 10^-3.
            # So exponent is -(start_idx + 1).
            b = -(start_idx + 1)
            
        # Format a: remove leading/trailing dots? No, a is like "1.23"
        # If s had only one digit after start, e.g., .5 -> s="5", start_idx=0
        # a = "5." -> should be "5" if integer? Yes, if a is integer, no decimal point.
        if '.' in a:
            int_a, frac_a = a.split('.')
            if not frac_a:
                a = int_a
            else:
                a = a # keep as is
        # Actually my construction s[start_idx] + "." + s[start_idx+1:] might create "5." if s[start_idx+1:] is empty
        # But s.rstrip('0') ensures trailing zeros are gone. If s was "50", s becomes "5", len=1, start_idx=0.
        # s[start_idx+1:] is empty. So a="5.". Split gives ("5", ""), int_a="5", frac_a="", a="5". Correct.
        # If s="500", s="5", same.
        # If s="05", s="5", same.
        # What if s="10"? start_idx=0. a="1.0" -> frac_a="0" -> "1.0" -> "1". Correct.
        
        # Finalize a
        if '.' in a:
            int_a, frac_a = a.split('.', 1)
            if frac_a == "":
                a = int_a
            elif frac_a == "0":
                a = int_a
            else:
                a = a
        else:
            a = a

        print(f"{a}E{b}")

    else:
        # Case 2: int_part is not "0" (e.g., "123.456" or "123")
        # The number is int_part . s
        # We need to find the first digit of int_part (which is non-zero because we stripped leading zeros)
        # Actually int_part might be "0" only if input was like 0.123 which falls into Case 1 logic?
        # My logic: if has_leading_dot, int_part="0". If not, int_part comes from string.
        # If input is "0.123", has_leading_dot=False, int_part="0", s="123". This is handled by Case 1?
        # Wait, my code:
        # if has_leading_dot: int_part = "0", s = s[1:]
        # else: dot_idx = s.find('.'), int_part = s[:dot_idx]
        # If input is "0.123", has_leading_dot=False. dot_idx=1. int_part="0". s="123".
        # Then int_part.lstrip('0') -> "". Then set to "0".
        # So "0.123" goes to Case 1 logic. Correct.
        
        # So int_part here is the integer part before decimal, stripped of leading zeros.
        # If int_part is "0", we are in the 0.XXX case.
        # If int_part is non-zero, we are in X.XXX case.
        
        # Re-evaluate logic inside else block of "if int_part == '0'"
        # Here int_part is non-zero string (e.g., "123" or "5").
        # We need to form a = d.dddd... where d is the first digit of int_part.
        # Exponent b = len(int_part) - 1.
        
        first_digit = int_part[0]
        remaining_int = int_part[1:] if len(int_part) > 1 else ""
        
        # Construct a: first_digit . remaining_int (if any) + s
        # But we need to merge remaining_int and s properly.
        # a = first_digit + "." + (remaining_int + s if remaining_int or s else remaining_int + s)
        # Actually simpler:
        # The sequence of digits after the first digit is: remaining_int + s
        # We need to put a dot after the first digit.
        
        digits_after_first = remaining_int + s
        if not digits_after_first:
            # e.g., input "5" -> int_part="5", s="" -> a="5", b=0
            a = first_digit
            b = len(int_part) - 1
        else:
            # a = first_digit . digits_after_first
            # But we need to ensure no extra zeros at start of digits_after_first?
            # int_part was stripped of leading zeros, so remaining_int has no leading zeros unless it's empty.
            # s was stripped of trailing zeros.
            # So digits_after_first is just the fractional digits.
            # However, we need to handle the decimal point placement.
            # a = first_digit + "." + digits_after_first
            # But if digits_after_first starts with zeros? e.g., 100.05 -> int_part="100", s="05"
            # remaining_int="00", s="05". digits_after_first="0005".
            # a = "1.0005". This is correct.
            
            # Wait, does digits_after_first contain leading zeros?
            # Yes, if the number was 100.05, remaining_int="00", s="05". Concatenated "0005".
            # We want a = 1.0005.
            # So a = first_digit + "." + digits_after_first.
            # Then check if a is integer.
            
            # One edge case: if digits_after_first is empty string, handled above.
            # If digits_after_first is not empty, we always have a decimal point?
            # Unless digits_after_first represents nothing? No, it's non-empty.
            # But we need to format a: if it's an integer (no fractional part), remove dot.
            # Here, since we have a dot and digits_after_first is non-empty, a has fractional part.
            # Unless digits_after_first is effectively zero? But we stripped trailing zeros from s.
            # If s was "000", s becomes "". Then digits_after_first = remaining_int.
            # e.g., 100.000 -> int_part="100", s="" -> remaining_int="00".
            # digits_after_first="00".
            # a = "1.00". This is not an integer representation "1".
            # We need to strip trailing zeros from the constructed a?
            # Or better: construct a, then normalize.
            
            # Let's rebuild:
            # We have the full string of digits excluding the decimal point: int_part + s
            # We want to split this into [first_digit] and [rest].
            # a_str = first_digit + "." + rest
            # Then normalize a_str: remove trailing zeros after dot, and if dot is last, remove it.
            
            full_digits = int_part + s
            # full_digits is like "10005" for 100.05? No, s="05", int_part="100" -> "10005".
            # We want 1.0005.
            # first = full_digits[0]
            # rest = full_digits[1:]
            # a_str = first + "." + rest
            # Normalize a_str:
            # Remove trailing zeros from the fractional part.
            # If fractional part becomes empty, remove dot.
            
            # Example 100.000 -> int_part="100", s="" -> full_digits="100"
            # first='1', rest="00"
            # a_str="1.00" -> remove trailing zeros -> "1." -> remove dot -> "1"
            # b = len(int_part) - 1 = 2.
            # Result "1E2". Correct.
            
            # Example 123.456 -> int_part="123", s="456" -> full_digits="123456"
            # first='1', rest="23456"
            # a_str="1.23456" -> no trailing zeros -> "1.23456"
            # b = 2.
            # Result "1.23456E2". Correct.
            
            # Example 0.00123 -> handled in Case 1.
            # Example 16 -> int_part="16", s="" -> full_digits="16"
            # first='1', rest="6" -> a="1.6", b=1. Result "1.6E1". Correct.
            
            # Implementation:
            first_digit = full_digits[0]
            rest = full_digits[1:]
            
            # Construct a with dot
            a_temp = first_digit + "." + rest
            
            # Remove trailing zeros from fractional part
            if '.' in a_temp:
                int_a, frac_a = a_temp.split('.', 1)
                frac_a = frac_a.rstrip('0')
                if not frac_a:
                    a = int_a
                else:
                    a = int_a + "." + frac_a
            else:
                a = a_temp
            
            b = len(int_part) - 1

            print(f"{a}E{b}")

solve()