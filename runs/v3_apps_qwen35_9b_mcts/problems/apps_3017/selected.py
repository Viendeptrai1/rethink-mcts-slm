import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    e = int(input_data[1])

    if e == 0:
        # 2^0 = 1. We need to count numbers containing "1".
        # However, the problem says "digits of 2^e". 2^0 is 1.
        # But wait, if e=0, 2^e=1. The string is "1".
        # Let's proceed with general logic.
        pass

    target_val = 1 << e
    target_s = str(target_val)
    m = len(target_s)

    if m == 0:
        # Should not happen for valid e >= 0
        print(0)
        return

    # Precompute powers of 10 for digit DP
    # n can be up to 9e18, so up to 19 digits.
    s_n = str(n)
    L = len(s_n)

    # dp[i][j][k][found]
    # i: current digit position (0 to L)
    # j: current match length (0 to m-1)
    # k: whether we are restricted by the prefix of n (tight constraint)
    # found: whether we have already found the target substring
    # We want to count numbers <= n that contain the substring.
    # It is easier to count total numbers (0 to n) and subtract those that do NOT contain the substring.
    # Or directly count those that DO contain.
    # Let's do direct counting: state includes 'found'.
    # dp[i][j][tight][found] = count of ways

    # To optimize, we can use memoization.
    # State: (index, match_len, tight, found)
    # index: 0..L
    # match_len: 0..m-1 (if found is True, match_len doesn't matter much, but we can keep it or set to m)
    # tight: 0 or 1
    # found: 0 or 1

    from functools import lru_cache

    @lru_cache(None)
    def dp(idx, match_len, tight, found):
        if found:
            # Once found, any subsequent digits are free (0-9)
            # Number of ways to fill remaining (L - idx) digits is 10^(L-idx)
            return 10 ** (L - idx)

        if idx == L:
            return 1 if found else 0

        limit = int(s_n[idx]) if tight else 9
        total = 0

        for digit in range(limit + 1):
            new_tight = tight and (digit == limit)
            
            # Update match length
            new_match = match_len
            if not found:
                # Try to extend the match
                # If match_len == m, it means we already found it, but we handled found=True above.
                # So match_len is always < m here.
                # Check if adding 'digit' completes the pattern
                # We need to check the last 'm' characters.
                # Current suffix before adding digit has length match_len.
                # We are adding 'digit'.
                # The new suffix of length up to m is: target_s[-(match_len+1):] + str(digit) ?
                # Actually, simpler: maintain the length of the longest prefix of target_s that is a suffix of the current number.
                
                # Let's simulate KMP failure function logic or just brute force since m is small (max 19 digits for 2^62? 2^62 is approx 4.6e18, so 19 digits).
                # Brute force check for small m is fine.
                
                # Current matched prefix length is match_len.
                # We append digit.
                # New potential match length:
                # Check if target_s[:match_len+1] ends with str(digit)? No.
                # We need to check if the new sequence ends with a prefix of target_s.
                
                # Construct the new suffix string of length min(m, match_len+1)
                # But we only know the last 'match_len' chars matched target_s[:match_len].
                # So the current string ends with target_s[:match_len].
                # Append digit d.
                # New string ends with target_s[:match_len] + str(d).
                # We need the longest prefix of target_s that is a suffix of this new string.
                
                # Since m is small, we can just check all lengths from min(m, match_len+1) down to 0.
                temp_str = target_s[:match_len] + str(digit)
                new_len = 0
                for length in range(min(m, len(temp_str)), -1, -1):
                    if temp_str.endswith(target_s[:length]):
                        new_len = length
                        break
                
                new_match = new_len
                new_found = False
                if new_match == m:
                    new_found = True
            else:
                new_found = True
                new_match = 0 # irrelevant

            if new_found:
                total += dp(idx + 1, 0, new_tight, True)
            else:
                total += dp(idx + 1, new_match, new_tight, False)

        return total

    # We need to count numbers from 0 to n.
    # The DP above counts numbers with exactly L digits (including leading zeros if we consider the number as a string of length L).
    # However, the problem asks for integers k (0 <= k <= n).
    # Our DP treats numbers as strings of length L with leading zeros.
    # Does "12560" contain "256"? Yes.
    # Does "0012560" contain "256"? Yes.
    # The substring check is on the decimal representation.
    # Standard decimal representation does NOT have leading zeros (except for the number 0 itself).
    # Example: 5 is "5", not "005".
    # If the target is "05", then "5" does not contain "05".
    # But 2^e never starts with 0. So the target string does not start with '0'.
    # Therefore, leading zeros in our padded representation will never help form the target string at the beginning, unless the target itself contains '0's which are matched against non-leading parts.
    # Wait, if target is "10", and number is 10.
    # Padded: "00...0010". The "10" is at the end.
    # If number is 5, padded "00...005". No "10".
    # The only issue is if the target string could be formed by crossing the boundary of leading zeros and actual digits.
    # Since target[0] != '0' (powers of 2: 1, 2, 4, 8, 16, 32... none start with 0), any match must start with a non-zero digit.
    # Leading zeros are '0'. So a match cannot start at a leading zero position.
    # Thus, matching in the padded string (with leading zeros) is equivalent to matching in the actual string, EXCEPT for the number 0 itself.
    # Number 0: padded "00...00". Does it contain target? Target starts with non-zero, so no.
    # So the count from DP (which considers 00...00 to s_n) is exactly the count of numbers in [0, n] containing the substring, provided target[0] != '0'.
    # Let's verify target[0] != '0'. 2^e for e>=0: 1, 2, 4, 8, 16... all start with 1,2,4,8. Correct.
    
    # One edge case: n=0.
    # s_n = "0". L=1.
    # DP runs for idx=0. limit=0. digit=0.
    # match_len=0. temp_str = "0". new_len=0 (since target starts with non-zero).
    # found=False.
    # Returns 0. Correct.
    
    # Another edge case: target is "1", n=0.
    # DP returns 0. Correct.
    
    # What if n is small, say n=5, target="1".
    # Numbers: 0,1,2,3,4,5. Contains "1": {1}. Count=1.
    # DP: L=1. s_n="5".
    # idx=0. limit=5.
    # digit=0: match "0" -> len 0. not found. dp(1,0,F,F) -> 0.
    # digit=1: match "1" -> len 1 -> found. dp(1,0,T,T) -> 10^0 = 1.
    # ...
    # digit=5: match "5" -> len 0.
    # Total = 1. Correct.
    
    # Wait, the DP state for 'found' returns 10^(L-idx).
    # If we are at idx=L and found=True, we return 1.
    # If we are at idx < L and found=True, we return 10^(L-idx).
    # This correctly counts all completions.
    
    # However, there is a subtle point: The number 0.
    # In our DP, the number 0 is represented as "00...00".
    # Does it get counted?
    # Only if found becomes True. Since target[0] != '0', found will never be True for all zeros.
    # So 0 is not counted, which is correct (0 does not contain "1", "2", etc).
    
    # Is there any case where leading zeros matter?
    # Suppose target = "01". But 2^e never is "01".
    # So we are safe.
    
    result = dp(0, 0, True, False)
    print(result)

if __name__ == '__main__':
    solve()