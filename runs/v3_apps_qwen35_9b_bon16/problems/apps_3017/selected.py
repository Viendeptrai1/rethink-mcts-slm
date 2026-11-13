import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    e = int(data[1])

    if e == 0:
        # 2^0 = 1. We need to count numbers in [0, n] that contain the digit '1' as a substring.
        # However, note that the problem says "digits of 2^e". 2^0 = 1, which is just the digit '1'.
        # But wait: does "1" appear in every number? No. Only numbers with at least one '1'.
        # However, there is a catch: the number 0 does not contain '1'.
        # So we count numbers in [0, n] containing digit '1'.
        # But the sample cases don't cover e=0. Let's rely on the general digit DP approach.
        pass

    power = 1 << e
    s = str(power)
    L = len(s)

    # If n is small, we can just check every number, but n can be up to 9e18.
    # So we must use Digit DP.

    # We want to count numbers k in [0, n] such that the string representation of k contains s.
    # Note: The problem says "contain the digits of 2^e as a substring".
    # Example: 2^3 = 8. Numbers containing "8": 8, 18, 28, ..., 80, 81, ...
    # Example: 2^5 = 32. Numbers containing "32": 32, 132, 232, 320, ...

    # Special case: if 2^e has more digits than n, then the only possible candidate is 2^e itself if 2^e <= n.
    # But our digit DP will handle this naturally if we implement it correctly.

    # Digit DP state:
    # index: current digit position we are placing (from left to right)
    # formed: boolean, has the pattern s been formed so far?
    # tight: boolean, are we restricted by the digits of n?
    # leading_zeros: boolean, are we currently placing leading zeros?

    # However, checking "has the pattern formed" is tricky because we need to track the suffix matching the prefix of s.
    # We can use KMP's failure function (pi array) to track the longest proper prefix of s that is also a suffix of the current string.

    # Let's precompute the KMP pi array for pattern s.
    # pi[i] = length of the longest proper prefix of s[0:i+1] that is also a suffix of s[0:i+1].

    def compute_pi(P):
        m = len(P)
        pi = [0] * m
        k = 0
        for q in range(1, m):
            while k > 0 and P[k] != P[q]:
                k = pi[k-1]
            if P[k] == P[q]:
                k += 1
            pi[q] = k
        return pi

    pi = compute_pi(s)

    # DP state: (index, match_len, tight, leading_zeros)
    # match_len: length of the longest prefix of s that is a suffix of the current number being built.
    # If match_len == L, then we have found the pattern.

    # Memoization dictionary
    from functools import lru_cache

    s_digits = [int(d) for d in s]

    @lru_cache(None)
    def dp(idx, match_len, tight, leading_zeros):
        if idx == len(str(n)):
            # If we have formed the pattern, count 1, else 0.
            return 1 if match_len == L else 0

        limit = int(str(n)[idx]) if tight else 9
        total = 0

        for digit in range(limit + 1):
            new_tight = tight and (digit == limit)
            new_leading = leading_zeros and (digit == 0)

            if new_leading:
                # Still in leading zeros, match_len remains 0.
                total += dp(idx + 1, 0, new_tight, True)
            else:
                # Not leading zeros anymore.
                # Update match_len using KMP logic.
                current_char = str(digit)
                # We want to extend the current match.
                # Current state: we have a suffix matching s[:match_len]
                # Now we add current_char.
                # The new match length is the length of the longest prefix of s that is a suffix of (s[:match_len] + current_char)
                
                # Simulate KMP transition:
                # q = match_len
                # while q > 0 and s[q] != current_char:
                #     q = pi[q-1]
                # if s[q] == current_char:
                #     q += 1
                # new_match = q
                
                # However, note: if match_len is already L, we don't need to continue, but our base case catches it at the end.
                # But actually, once match_len reaches L, we can stop and count all subsequent states as valid.
                # To optimize, we can have a state "already_found" but let's stick to match_len and check at the end.
                # Alternatively, we can cap match_len at L, but the transition above might go beyond if not careful? 
                # Actually, if match_len == L, we consider it found. But in our transition, if match_len is L, we don't really need to compute further.
                # However, the base case checks at the end. So we can let match_len be L and then any further transitions? 
                # But if match_len is L, then we have already found it. We can just set a flag or cap it.
                # Let's cap match_len at L. If it reaches L, it stays L.
                
                if match_len == L:
                    new_match = L
                else:
                    q = match_len
                    while q > 0 and s_digits[q] != digit:
                        q = pi[q-1]
                    if s_digits[q] == digit:
                        q += 1
                    new_match = q
                
                total += dp(idx + 1, new_match, new_tight, False)

        return total

    # We need to count numbers in [0, n].
    # Our DP counts numbers in [0, n] that satisfy the condition.
    # However, note: the number 0 is represented as "0". 
    # If the pattern is "0", then 0 should be counted. But 2^e is never 0.
    # The smallest power is 2^0=1. So pattern is never "0".
    # Leading zeros in our DP mean we are building numbers with fewer digits.
    # When we finish, if we were in leading_zeros all the way, it means the number is 0.
    # Does 0 contain the pattern? Only if the pattern is "0", which it isn't.
    # So our DP correctly returns 0 for the case of number 0 (unless pattern is "0").
    # But wait: what if the pattern is "1"? Then 0 does not contain "1", so it should not be counted.
    # Our DP: for number 0, we go through all leading_zeros until the end, and match_len remains 0.
    # At the end, 0 != L (since L>=1), so it returns 0. Correct.

    # However, there is one more issue: the problem says "digits of 2^e". 
    # What if 2^e is "1"? Then we are counting numbers containing "1".
    # Our DP should work.

    # But note: the problem says "distinct integers k". Our DP counts distinct integers.

    result = dp(0, 0, True, True)
    print(result)

if __name__ == "__main__":
    solve()