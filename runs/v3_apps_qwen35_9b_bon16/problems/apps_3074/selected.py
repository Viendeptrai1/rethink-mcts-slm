import sys

# Increase recursion depth just in case, though we will use an iterative DP approach.
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s_str = input_data[1]
    
    MOD = 10**9 + 7
    
    # We need to count the number of non-empty subsets of characters (indices) 
    # such that when the characters are concatenated in some order, 
    # the resulting number has no leading zeros and is divisible by 3.
    
    # Key Observations:
    # 1. A number is divisible by 3 if and only if the sum of its digits is divisible by 3.
    #    The order of digits does not affect divisibility by 3.
    # 2. "No leading zeros" constraint:
    #    - If the subset contains only '0's, it is invalid (leading zero unless the number is just "0", 
    #      but a single "0" has no leading zero. However, if the subset has length > 1 and all are '0', 
    #      e.g., "00", "000", these have leading zeros. 
    #      Wait, the problem says "concatenated together in some way to form a number with no leading zeros".
    #      If we have a set of digits {0, 0}, can we form a number with no leading zeros? 
    #      We can form "00" (leading zero) or "00" (same). No valid permutation exists for {0,0} to have no leading zero.
    #      If we have {0}, we form "0". "0" is a valid number with no leading zero (0 is not considered to have a leading zero).
    #      So, a subset is valid iff:
    #        a) The sum of digits is divisible by 3.
    #        b) We can arrange them to not start with 0.
    #           - This is possible if the subset contains at least one non-zero digit.
    #           - Exception: If the subset is exactly {"0"} (one zero), it forms "0", which is valid.
    #           - If the subset has multiple zeros and no non-zeros (e.g., {0, 0}), any permutation starts with 0 -> invalid.
    #           - If the subset has at least one non-zero, we can always put that non-zero first -> valid (provided sum % 3 == 0).
    
    # So the conditions for a subset of indices to be valid:
    # 1. Sum of digits % 3 == 0.
    # 2. Either (count of zeros == 1 AND total count == 1) OR (count of non-zeros >= 1).
    #    Actually, let's refine:
    #    - Case A: Subset contains at least one non-zero digit. Then we can arrange it to start with non-zero. 
    #      Valid if sum % 3 == 0.
    #    - Case B: Subset contains ONLY zero digits.
    #      - If size is 1: "0" -> Valid (sum=0, divisible by 3).
    #      - If size > 1: e.g., "00", "000" -> All permutations start with 0 -> Invalid.
    
    # Therefore:
    # Valid subsets are those where:
    # (sum % 3 == 0) AND ( (len(subset) == 1 AND char is '0') OR (exists non-zero in subset) )
    
    # Let's count:
    # Total subsets with sum % 3 == 0.
    # Subtract subsets that have sum % 3 == 0 but are invalid due to leading zero constraints.
    # Which subsets have sum % 3 == 0 but are invalid?
    # 1. Subsets consisting of only zeros with size > 1.
    #    Note: A subset of only zeros has sum = 0, which is divisible by 3.
    #    So any subset of only zeros with size > 1 is counted in "sum % 3 == 0" but is invalid.
    # 2. Subsets consisting of only zeros with size 1? 
    #    Size 1 zero subset: sum=0 (div by 3). Valid? Yes ("0"). So we don't subtract it.
    
    # So the strategy:
    # 1. Count all non-empty subsets with sum % 3 == 0.
    # 2. Subtract the number of subsets consisting entirely of '0's with length > 1.
    
    # Step 1: Count subsets with sum % 3 == 0.
    # We can use DP.
    # dp[rem] = number of subsets formed so far with digit sum % 3 == rem.
    # Initialize: dp[0] = 1 (empty set), dp[1] = 0, dp[2] = 0.
    # Iterate through each digit d in the string.
    # new_dp = dp[:]
    # For each rem in 0..2:
    #   new_rem = (rem + d) % 3
    #   new_dp[new_rem] = (new_dp[new_rem] + dp[rem]) % MOD
    # Update dp = new_dp
    # The number of non-empty subsets with sum % 3 == 0 is (dp[0] - 1) because we start with empty set.
    
    # Step 2: Count subsets of only '0's with length > 1.
    # Let Z be the total count of '0' characters in the string.
    # The number of non-empty subsets of these Z zeros is 2^Z - 1.
    # We want subsets of size > 1.
    # Total non-empty subsets of zeros = 2^Z - 1.
    # Subsets of size 1 = Z.
    # Subsets of size > 1 = (2^Z - 1) - Z.
    # These are the invalid ones that were included in Step 1 (since their sum is 0).
    # Note: We must ensure Z >= 1. If Z=0, count is 0.
    
    # Final Answer = (Total_subsets_sum_div_3 - Invalid_zero_subsets) % MOD.
    
    # DP for Step 1
    dp = [0] * 3
    dp[0] = 1
    
    for char in s_str:
        d = int(char)
        # Update dp in reverse or use temporary array to avoid using updated values from current step
        # Since we are adding a new element, it can combine with any existing subset.
        # new_dp[r] = dp[r] (not including new char) + sum(dp[(r - d) % 3]) (including new char)
        # Actually simpler: iterate all previous states and add transitions.
        
        new_dp = [0] * 3
        # Option 1: Don't include current digit in the subset
        for i in range(3):
            new_dp[i] = (new_dp[i] + dp[i]) % MOD
        
        # Option 2: Include current digit
        # If current subset sum % 3 was r, new sum is (r + d) % 3
        # So we add dp[r] to new_dp[(r+d)%3]
        for i in range(3):
            if dp[i] == 0:
                continue
            next_rem = (i + d) % 3
            new_dp[next_rem] = (new_dp[next_rem] + dp[i]) % MOD
        
        dp = new_dp

    total_div_3 = (dp[0] - 1 + MOD) % MOD  # Subtract empty set
    
    # Step 2: Count invalid zero-only subsets of size > 1
    count_zeros = s_str.count('0')
    if count_zeros > 0:
        # Total non-empty subsets of zeros: 2^count_zeros - 1
        # Subsets of size 1: count_zeros
        # Invalid (size > 1): (2^count_zeros - 1) - count_zeros
        # Simplify: 2^count_zeros - 1 - count_zeros
        
        # Calculate 2^count_zeros % MOD
        pow2 = pow(2, count_zeros, MOD)
        invalid_count = (pow2 - 1 - count_zeros + MOD) % MOD
    else:
        invalid_count = 0
    
    ans = (total_div_3 - invalid_count + MOD) % MOD
    print(ans)

if __name__ == '__main__':
    solve()