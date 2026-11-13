import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        n = int(input_data[0])
        s_str = input_data[1]
    except Exception:
        return

    MOD = 10**9 + 7

    # Count digits 0-9
    counts = [0] * 10
    for ch in s_str:
        counts[int(ch)] += 1

    # Precompute powers of 2 for combinations
    # We need up to n
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD

    # Check if a digit d can be part of a valid number (non-zero leading, divisible by 3)
    # A single digit d is valid if d != 0 and d % 3 == 0
    # However, the problem says "concatenated together in some way to form a number with no leading zeros that is also divisible by 3"
    # This implies we are forming a number from a subset of digits.
    # Key insight: A number is divisible by 3 iff the sum of its digits is divisible by 3.
    # Leading zeros constraint: The first digit of the formed number cannot be 0.
    # So, a subset of digits can form a valid number if:
    # 1. The subset is not empty.
    # 2. The sum of digits in the subset is divisible by 3.
    # 3. The subset contains at least one non-zero digit (to avoid leading zero issue if we consider the number formed).
    #    Actually, if a subset consists only of zeros, say {0, 0}, can we form a number? 
    #    "no leading zeros" -> 00 is not allowed, 0 is allowed? 
    #    Usually, a number "0" has no leading zeros. But "00" does.
    #    If the subset is {0}, the number is 0. Is 0 divisible by 3? Yes. Does it have leading zeros? 
    #    Technically, the representation "0" is fine. But if we have multiple zeros, we can't form a number without leading zeros unless we pick just one zero?
    #    The problem says "concatenated together in some way". If we have {0, 0}, we can form "0" (using one 0) or "00" (invalid).
    #    Since we just need to know if there EXISTS a way to concatenate them to form a valid number.
    #    If the subset has at least one non-zero digit, we can put that first, then the rest. Sum is same. Divisibility by 3 depends only on sum.
    #    If the subset has ONLY zeros:
    #       - If size is 1: "0" -> valid (divisible by 3, no leading zero).
    #       - If size > 1: Any permutation starts with 0, so "00...", which has leading zeros. Invalid.
    #    So a subset of all zeros is valid ONLY if its size is 1.

    # Let's re-read carefully: "define a subset S of characters from B 'valid' iff the characters in S can be concatenated together in some way to form a number with no leading zeros that is also divisible by 3."
    # This means: Does there exist a permutation of the subset that forms a valid number?
    # Case 1: Subset contains at least one non-zero digit.
    #    We can arrange the non-zero digit first. The resulting number has no leading zero.
    #    The number is divisible by 3 iff sum(digits) % 3 == 0.
    #    So any subset with at least one non-zero digit is valid IF sum % 3 == 0.
    # Case 2: Subset contains only zeros.
    #    If size == 1: "0" is valid.
    #    If size > 1: Any arrangement is "00...0", which has leading zeros. Invalid.
    #    So a subset of only zeros is valid iff size == 1.

    # Strategy:
    # Total valid subsets = (Subsets with sum % 3 == 0 AND (has non-zero OR (only zeros AND size==1)))
    # = (Subsets with sum % 3 == 0 AND has non-zero) + (Subsets of only zeros with size == 1)
    
    # Note: A subset of only zeros with size 1 has sum 0, which is divisible by 3.
    # So "Subsets with sum % 3 == 0 AND has non-zero" excludes the all-zero subsets.
    # Then we add back the specific case of a single zero.
    
    # Let's calculate:
    # 1. Count subsets with sum % 3 == 0.
    # 2. Subtract subsets with sum % 3 == 0 that consist ONLY of zeros.
    #    Which are: 
    #       - Empty set? Sum 0. But empty set cannot form a number. Problem implies non-empty? 
    #         "form a number" usually implies non-empty. Also "no leading zeros" applies to numbers.
    #         Let's assume non-empty.
    #       - Single zero: Valid.
    #       - Multiple zeros: Invalid.
    #    So among "only zeros" subsets, only the single zero is valid.
    #    Wait, my logic above:
    #    Valid = (Sum%3==0 AND (has_nonzero OR (only_zeros AND size==1)))
    #    = (Sum%3==0 AND has_nonzero) + (only_zeros AND size==1 AND Sum%3==0)
    #    Since sum of zeros is 0, Sum%3==0 is always true for any subset of zeros.
    #    So we need: (Count of subsets with sum%3==0 that have at least one non-zero) + (1 if there is at least one '0' in input else 0).
    
    # How to count subsets with sum%3==0 that have at least one non-zero?
    # Total subsets with sum%3==0 (including those with only zeros and empty) MINUS (subsets with only zeros and sum%3==0).
    # Subsets with only zeros and sum%3==0:
    #    - Empty set: sum 0. (Exclude empty set from final answer as it can't form a number)
    #    - Single zero: sum 0. (Include this)
    #    - Two or more zeros: sum 0. (Exclude these because they can't form a valid number due to leading zeros)
    #    
    # So, let A = Total non-empty subsets with sum % 3 == 0.
    # Let B = Subsets consisting ONLY of zeros that are valid.
    #    B = 1 if count[0] >= 1 else 0. (Because only the single zero subset works. Empty is not a number. Multiple zeros fail leading zero check).
    # But wait, does A include the single zero? Yes, because sum=0.
    # Does A include multiple zeros? Yes, sum=0.
    # Does A include empty? Usually "subset" includes empty, but "form a number" implies non-empty.
    # Let's define:
    # Total non-empty subsets with sum % 3 == 0 = (Total subsets with sum % 3 == 0) - (1 if empty set has sum%3==0 else 0).
    # Empty set sum is 0, so it is included in "sum%3==0". So subtract 1.
    # Now, from these non-empty subsets with sum%3==0, we must remove those that consist ONLY of zeros and have size > 1.
    # Because those cannot form a valid number (leading zeros).
    # The subsets of only zeros with size > 1 are: C(count[0], 2) + C(count[0], 3) + ...
    # Sum of C(n, k) for k=2 to n is 2^n - C(n, 0) - C(n, 1) = 2^n - 1 - n.
    # So, number of invalid "only zeros" subsets (size > 1) = 2^(count[0]) - 1 - count[0].
    # Note: This formula gives 0 if count[0] < 2.
    #    If count[0] = 0: 1 - 1 - 0 = 0. Correct.
    #    If count[0] = 1: 2 - 1 - 1 = 0. Correct.
    #    If count[0] = 2: 4 - 1 - 2 = 1. ({0,0} is the only one). Correct.
    
    # So the algorithm:
    # 1. Calculate total non-empty subsets with sum % 3 == 0.
    #    To do this efficiently, we group digits by remainder mod 3.
    #    Let c0 = count of digits with d%3==0 (includes 0, 3, 6, 9)
    #    Let c1 = count of digits with d%3==1 (1, 4, 7)
    #    Let c2 = count of digits with d%3==2 (2, 5, 8)
    #    
    #    We need to choose subsets from these groups such that (sum of remainders) % 3 == 0.
    #    Possible combinations of counts (k0 from c0, k1 from c1, k2 from c2):
    #    (k1 % 3 + k2 % 3) % 3 == 0.
    #    Cases:
    #    1. k1 % 3 == 0 and k2 % 3 == 0.
    #       k1 can be 0, 3, 6... -> ways = sum_{i=0}^{floor(c1/3)} C(c1, 3i)
    #       k2 can be 0, 3, 6... -> ways = sum_{j=0}^{floor(c2/3)} C(c2, 3j)
    #       Total ways for this case = (sum C(c1, 3i)) * (sum C(c2, 3j))
    #    2. k1 % 3 == 1 and k2 % 3 == 2.
    #       k1 = 1, 4, 7... -> ways = sum C(c1, 3i+1)
    #       k2 = 2, 5, 8... -> ways = sum C(c2, 3j+2)
    #       Total = (sum C(c1, 3i+1)) * (sum C(c2, 3j+2))
    #    3. k1 % 3 == 2 and k2 % 3 == 1.
    #       k1 = 2, 5, 8... -> ways = sum C(c1, 3i+2)
    #       k2 = 1, 4, 7... -> ways = sum C(c2, 3j+1)
    #       Total = (sum C(c1, 3i+2)) * (sum C(c2, 3j+1))
    #    
    #    Also, we can choose any number from c0 (since 0%3==0).
    #    Ways to choose from c0 = 2^c0.
    #    
    #    So Total Subsets with sum%3==0 = 2^c0 * [ (S0_1 * S0_2) + (S1_1 * S2_2) + (S2_1 * S1_2) ]
    #    Where Sx_y is sum of C(c_x, 3k + y).
    #    
    #    We can compute these sums using dynamic programming or combinatorics.
    #    Since N <= 200,000, we cannot iterate all subsets. But we can compute the sums of binomial coefficients with step 3 efficiently.
    #    There is a known identity or we can use DP.
    #    Let dp[i][r] = sum of C(i, k) where k % 3 == r.
    #    We can compute this in O(N) or O(1) with precomputed factorials? No, we need sums of every 3rd.
    #    Actually, we can use roots of unity filter or simple DP.
    #    Given N=200,000, O(N) is fine.
    #    We can compute an array `ways[r]` for a given count `n` where ways[r] = sum_{k} C(n, k) with k%3==r.
    #    Recurrence:
    #    ways[r] for n = sum_{k} C(n, k) where k%3==r.
    #    C(n, k) = C(n-1, k) + C(n-1, k-1).
    #    So ways[r](n) = ways[r](n-1) + ways[r-1](n-1). (Indices mod 3)
    #    Base case: n=0 -> ways[0]=1, others 0.
    #    We can compute this iteratively for c1 and c2.
    
    # Implementation details:
    # Function get_sums(n): returns [s0, s1, s2] where s_r = sum C(n, k) for k%3==r.
    # Since we only need this for c1 and c2, and c1+c2 <= N, we can just run the DP for each.
    # Complexity: O(c1 + c2) = O(N).
    
    def get_binomial_sums_mod3(n):
        # Returns [sum C(n, k) for k%3==0, k%3==1, k%3==2]
        if n == 0:
            return [1, 0, 0]
        
        # dp[r] will store the current sum for remainder r
        # Initialize for n=0
        dp = [1, 0, 0]
        
        for i in range(1, n + 1):
            new_dp = [0, 0, 0]
            # new_dp[r] = dp[r] + dp[r-1] (mod 3 index)
            # r=0: dp[0] + dp[2]
            # r=1: dp[1] + dp[0]
            # r=2: dp[2] + dp[1]
            new_dp[0] = (dp[0] + dp[2]) % MOD
            new_dp[1] = (dp[1] + dp[0]) % MOD
            new_dp[2] = (dp[2] + dp[1]) % MOD
            dp = new_dp
        return dp

    c0 = counts[0] + counts[3] + counts[6] + counts[9]
    c1 = counts[1] + counts[4] + counts[7]
    c2 = counts[2] + counts[5] + counts[8]

    s0_1, s1_1, s2_1 = get_binomial_sums_mod3(c1)
    s0_2, s1_2, s2_2 = get_binomial_sums_mod3(c2)

    term1 = (s0_1 * s0_2) % MOD
    term2 = (s1_1 * s2_2) % MOD
    term3 = (s2_1 * s1_2) % MOD

    total_comb = (term1 + term2 + term3) % MOD
    total_subsets_sum0 = (pow2[c0] * total_comb) % MOD

    # This total_subsets_sum0 includes:
    # 1. Empty set (sum 0)
    # 2. Subsets of only zeros (any size)
    # 3. Subsets with non-zeros and sum%3==0
    # 4. Subsets with mixed zeros and non-zeros and sum%3==0
    
    # We want: (Subsets with sum%3==0 AND (has_nonzero OR (only_zeros AND size==1)))
    # = (Total non-empty subsets with sum%3==0) - (Subsets of only zeros with size > 1)
    # Note: "Total non-empty" = total_subsets_sum0 - 1 (remove empty set)
    # "Subsets of only zeros with size > 1" = 2^c0 - 1 - c0 (if c0 >= 2, else 0)
    #    Formula 2^c0 - 1 - c0 works for c0=0 (1-1-0=0), c0=1 (2-1-1=0), c0=2 (4-1-2=1).
    
    invalid_only_zeros = (pow2[c0] - 1 - c0) % MOD
    if invalid_only_zeros < 0:
        invalid_only_zeros += MOD

    non_empty_sum0 = (total_subsets_sum0 - 1 + MOD) % MOD
    valid = (non_empty_sum0 - invalid_only_zeros + MOD) % MOD

    print(valid)

if __name__ == '__main__':
    solve()