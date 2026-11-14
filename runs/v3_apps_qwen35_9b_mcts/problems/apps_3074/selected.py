import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        n = int(input_data[0])
        s = input_data[1]
    except IndexError:
        return

    MOD = 10**9 + 7

    # Count digits by their remainder modulo 3
    # rem 0: digits 0, 3, 6, 9
    # rem 1: digits 1, 4, 7
    # rem 2: digits 2, 5, 8
    c0 = 0
    c1 = 0
    c2 = 0

    for ch in s:
        d = int(ch)
        r = d % 3
        if r == 0:
            c0 += 1
        elif r == 1:
            c1 += 1
        else:
            c2 += 1

    # Calculate powers of 2 for combinations
    # We need 2^c0, 2^c1, 2^c2
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD

    # Total subsets with sum % 3 == 0
    # Case 1: Only digits with rem 0 are chosen (any non-empty subset of c0)
    # If c0 > 0, we have (2^c0 - 1) non-empty subsets. If c0 == 0, 0.
    # But wait, the problem says "no leading zeros".
    # If the subset forms the number "0", is it valid?
    # "form a number with no leading zeros". Usually "0" is allowed as a number, but "05" is not.
    # However, if we pick a subset of digits that includes '0's and other digits, we must ensure we don't form a number with leading zero.
    # But the problem says "concatenated together in some way". This implies we can reorder the digits in the subset.
    # If a subset contains at least one non-zero digit, we can always arrange them such that no leading zero occurs (put a non-zero first).
    # If a subset contains ONLY zeros, the only number we can form is "0...0" which simplifies to "0".
    # Does "0" have a leading zero? Technically, the number 0 is written as "0", which does not have a leading zero in the standard sense (the digit 0 is the number itself).
    # However, often in such problems, "no leading zeros" implies the string representation must not start with '0' unless the number is exactly 0.
    # Let's re-read carefully: "form a number with no leading zeros".
    # If the subset is {'0'}, the number is 0. String "0". Is "0" considered to have a leading zero? Usually no.
    # If the subset is {'0', '0'}, the number is 0. String "0".
    # If the subset is {'0', '1'}, we can form "10" (valid) or "01" (invalid). Since we can choose the order, we choose "10". So it's valid.
    # The only problematic case is if we are forced to have a leading zero. We are only forced if all digits are '0'.
    # If all digits are '0', the number formed is 0. Is 0 valid?
    # Let's look at Sample 2: Input "11". Digits are 1, 1. Sum=2. No subset sum divisible by 3. Output 0. Correct.
    # Sample 1: "361". Digits: 3 (rem 0), 6 (rem 0), 1 (rem 1).
    # Subsets with sum % 3 == 0:
    # {3} -> 3 (valid)
    # {6} -> 6 (valid)
    # {3, 6} -> 36 (valid)
    # {1} -> 1 (no)
    # {3, 1} -> 4 (no)
    # {6, 1} -> 7 (no)
    # {3, 6, 1} -> 10 (no)
    # Total 3. Output 3. Correct.
    # What if input is "0"? Subset {0}. Sum 0. Number 0. Valid?
    # If "0" is valid, then for input "0", answer should be 1.
    # If "0" is invalid (because it's a leading zero?), answer 0.
    # Standard interpretation: The number 0 is represented as "0", which is not a leading zero. Leading zero means a zero before a non-zero digit (e.g., 05).
    # So subsets consisting entirely of zeros should be counted as 1 valid number (the number 0).
    # However, if the subset has multiple zeros, say {0, 0}, the number is still 0. It's the same number.
    # The problem asks for the number of "valid subsets". A subset is a set of indices (or values if distinct, but here indices matter for subsets of a string).
    # "subset S of characters from B". This usually means a subset of indices.
    # So {index of first 0} and {index of second 0} are different subsets if there are two 0s.
    # Both form the number 0. Both are valid.
    # So we count the number of subsets whose digits sum to 0 mod 3.
    # The "no leading zeros" constraint is satisfied if:
    # 1. The subset contains at least one non-zero digit. We can always order them to avoid leading zero.
    # 2. The subset contains only zero digits. The number formed is 0. "0" is valid.
    # Therefore, the condition "no leading zeros" does not exclude any subset that sums to 0 mod 3, provided we can form a valid representation.
    # Since we can reorder, any subset with at least one non-zero is valid.
    # Any subset with only zeros forms "0", which is valid.
    # So we just need to count the number of subsets of digits whose sum is divisible by 3.

    # Let A = 2^c0, B = 2^c1, C = 2^c2.
    # We want the coefficient of x^0 in the expansion of:
    # (1 + x^0)^(c0) * (1 + x^1)^(c1) * (1 + x^2)^(c2) mod (x^3 - 1)
    # Actually, we just need the sum of coefficients where exponent % 3 == 0.
    # Let P0 = 2^c0, P1 = 2^c1, P2 = 2^c2.
    # The generating function for rem 0 digits is (1 + y^0)^c0 = (1+1)^c0 = 2^c0. All terms are y^0.
    # For rem 1 digits: (1 + y^1)^c1 = sum_{k=0}^{c1} C(c1, k) y^k.
    # For rem 2 digits: (1 + y^2)^c2 = sum_{k=0}^{c2} C(c2, k) y^(2k).
    # We need the sum of coefficients of y^m where m % 3 == 0.
    # Let F(y) = (1+y)^c1 * (1+y^2)^c2.
    # We want sum of coeffs of y^m in F(y) * 2^c0 where m % 3 == 0.
    # This is equivalent to 2^c0 * (sum of coeffs of y^m in F(y) where m%3==0).
    # Let S_k be the sum of coefficients of y^m in F(y) where m % 3 == k.
    # We need S_0.
    # Using roots of unity filter:
    # S_0 = (F(1) + F(w) + F(w^2)) / 3, where w = e^(2*pi*i/3).
    # F(1) = (1+1)^c1 * (1+1^2)^c2 = 2^c1 * 2^c2 = 2^(c1+c2).
    # F(w) = (1+w)^c1 * (1+w^2)^c2.
    # Note that 1+w = -w^2 and 1+w^2 = -w.
    # So F(w) = (-w^2)^c1 * (-w)^c2 = (-1)^(c1+c2) * w^(-2c1) * w^c2 = (-1)^(c1+c2) * w^(c2 - 2c1).
    # Similarly, F(w^2) = (1+w^2)^c1 * (1+w^4)^c2 = (1+w^2)^c1 * (1+w)^c2.
    # 1+w^2 = -w, 1+w = -w^2.
    # F(w^2) = (-w)^c1 * (-w^2)^c2 = (-1)^(c1+c2) * w^c1 * w^(-2c2) = (-1)^(c1+c2) * w^(c1 - 2c2).
    # Let K = (-1)^(c1+c2).
    # F(w) = K * w^(c2 - 2c1).
    # F(w^2) = K * w^(c1 - 2c2).
    # Note that w^3 = 1.
    # Exponent mod 3:
    # e1 = (c2 - 2c1) % 3
    # e2 = (c1 - 2c2) % 3
    # w^e1 is a complex number, but we are working in integers modulo 10^9+7?
    # Wait, the problem asks for the count modulo 10^9+7.
    # The roots of unity method works over complex numbers, but we can simulate w using modular arithmetic if we map w to a primitive 3rd root of unity in the field Z_p.
    # Does Z_p have a primitive 3rd root of unity?
    # p = 10^9 + 7. p % 3 = (1+0+7)%3 = 8%3 = 2.
    # Since p % 3 != 1, there is no primitive 3rd root of unity in Z_p.
    # So we cannot use the standard roots of unity filter directly in Z_p.
    # Alternative approach:
    # We can compute the sums iteratively or using DP.
    # Let dp[r] be the number of ways to choose a subset of the processed digits such that the sum of remainders is r mod 3.
    # Initially dp[0] = 1, dp[1] = 0, dp[2] = 0.
    # For each digit with remainder r:
    # new_dp[0] = dp[0] + dp[r] (if we pick the digit, sum increases by r; if we don't, sum stays)
    # Actually, for each digit, we have two choices: include or exclude.
    # If we include a digit with remainder r, the new sum is (old_sum + r) % 3.
    # So:
    # new_dp[k] = dp[k] (exclude) + dp[(k - r) % 3] (include)
    # This is O(N). N <= 200,000. This is perfectly fine.
    # We don't need the complex roots of unity trick. Just simple DP.

    dp = [0, 0, 0]
    dp[0] = 1

    for ch in s:
        d = int(ch)
        r = d % 3
        # Update dp in reverse or use temp array
        # new_dp[k] = dp[k] + dp[(k - r) % 3]
        # Let's compute new values
        n0 = (dp[0] + dp[(0 - r) % 3]) % MOD
        n1 = (dp[1] + dp[(1 - r) % 3]) % MOD
        n2 = (dp[2] + dp[(2 - r) % 3]) % MOD
        dp = [n0, n1, n2]

    # The result is dp[0].
    # This counts the empty set as well (sum 0).
    # The problem asks for "valid subsets".
    # Does the empty set count?
    # "form a number with no leading zeros".
    # An empty set cannot form a number. So it is not valid.
    # So we subtract 1 from dp[0].
    # However, we must check if the problem implies non-empty subsets.
    # "subset S of characters ... can be concatenated ... to form a number".
    # Empty set cannot form a number. So exclude empty set.
    # Result = (dp[0] - 1 + MOD) % MOD.

    ans = (dp[0] - 1 + MOD) % MOD
    print(ans)

if __name__ == '__main__':
    solve()