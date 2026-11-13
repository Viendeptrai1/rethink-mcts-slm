import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n_bin = input_data[0]
    k = int(input_data[1])
    
    MOD = 10**9 + 7
    L = len(n_bin)
    
    # Precompute popcount for numbers up to 1000 (since max bits in n is 1000)
    # Actually, the intermediate value after one step is at most 1000 (number of bits)
    # So we need popcount for numbers up to 1000.
    MAX_VAL = 1005
    pop = [0] * MAX_VAL
    for i in range(1, MAX_VAL):
        pop[i] = pop[i >> 1] + (i & 1)
    
    # Compute steps[i]: minimum operations to reduce i to 1
    # If i is 1, steps = 0
    # If i > 1, steps = 1 + steps[pop[i]]
    steps = [0] * MAX_VAL
    for i in range(2, MAX_VAL):
        steps[i] = 1 + steps[pop[i]]
    
    # If k == 0, the only special number is 1.
    # We need to count numbers <= n that reduce to 1 in 0 steps.
    # Only 1 satisfies this.
    if k == 0:
        if n_bin == '1':
            print(1)
        else:
            print(0)
        return
    
    # If k == 1, we need numbers x such that steps[x] == 1.
    # This means 1 + steps[pop[x]] == 1 => steps[pop[x]] == 0 => pop[x] == 1.
    # So x must have exactly 1 bit set.
    # But wait, the definition says "minimum number of operations to reduce it to 1 is k".
    # If x=1, operations=0.
    # If x has 1 bit set and x != 1, then pop[x]=1, next is 1, so 1 op.
    # So for k=1, we count numbers with exactly 1 bit set, excluding 1? 
    # No, if x=1, ops=0. If x=2 (10), pop=1 -> 1 op.
    # So for k=1, we count numbers with popcount=1, except 1 itself? 
    # Actually, if pop[x]=1, then next is 1. So 1 op.
    # So any number with exactly 1 bit set (and > 1) works.
    # But what if x=1? ops=0. So not included for k=1.
    # So for k=1, we count numbers with popcount=1, excluding 1.
    
    # General approach:
    # We need to count x in [1, n] such that steps[x] == k.
    # Note: steps[x] depends only on pop[x].
    # Let c = pop[x]. Then steps[x] = 1 + steps[c] (if c > 1), or 0 if c=1 (and x=1).
    # Actually, if x=1, pop[x]=1, but we stop at 1, so 0 ops.
    # If x > 1, we do one op to get pop[x], then continue.
    # So:
    # If x = 1: ops = 0.
    # If x > 1: ops = 1 + ops(pop[x]).
    
    # Therefore:
    # If k = 0: only x=1.
    # If k >= 1: we need 1 + ops(pop[x]) = k => ops(pop[x]) = k - 1.
    # Let target = k - 1.
    # We need to count x in [1, n] such that:
    #   x > 1 AND ops(pop[x]) == target.
    # Note: if pop[x] = 1, then ops(1) = 0. So if target=0, we need pop[x]=1 and x>1.
    # If target > 0, we need pop[x] = c such that ops(c) = target.
    
    target = k - 1
    
    # Find all c in [1, 1000] such that ops(c) == target.
    # Note: c can be 1? If c=1, ops(c)=0. So if target=0, c=1 is valid.
    valid_c = []
    for c in range(1, MAX_VAL):
        if steps[c] == target:
            valid_c.append(c)
    
    # Now we need to count x in [1, n] such that pop[x] is in valid_c and x > 1.
    # But note: if pop[x] = 1, then x has exactly 1 bit set.
    # If x has 1 bit set, then x is a power of 2.
    # If x=1, pop[x]=1, but we require x>1 for k>=1.
    # So if 1 is in valid_c, we count numbers with pop[x]=1 in [1, n] and subtract 1 (for x=1).
    # If 1 is not in valid_c, then we don't count x=1 anyway.
    
    # We will count numbers in [1, n] with pop[x] in valid_c, then subtract 1 if 1 is in valid_c (because x=1 is not allowed for k>=1).
    
    # Digit DP to count numbers <= n with popcount in valid_c.
    # n is given as binary string.
    
    # dp[i][j] = number of ways to fill suffix starting at i with j bits set so far,
    # but we need to handle the tight constraint.
    # Standard digit DP:
    # state: (index, count, tight)
    # index: current bit position (from 0 to L-1)
    # count: number of bits set so far
    # tight: boolean, true if we are restricted by n's prefix
    
    # We want to sum over c in valid_c: count of x in [1, n] with pop[x] == c.
    # Then subtract 1 if 1 is in valid_c.
    
    # Let's compute total count of x in [1, n] with pop[x] in valid_c.
    
    # DP state:
    # memo[index][count][tight]
    # index: 0..L
    # count: 0..L
    # tight: 0 or 1
    
    memo = {}
    
    def dp(idx, cnt, tight):
        if cnt > L:
            return 0
        if idx == L:
            return 1 if cnt in valid_c else 0
        
        state = (idx, cnt, tight)
        if state in memo:
            return memo[state]
        
        res = 0
        limit = int(n_bin[idx]) if tight else 1
        
        for digit in range(limit + 1):
            new_tight = tight and (digit == limit)
            new_cnt = cnt + (1 if digit == 1 else 0)
            res = (res + dp(idx + 1, new_cnt, new_tight)) % MOD
        
        memo[state] = res
        return res
    
    # Count numbers in [0, n] with popcount in valid_c.
    # But our DP counts from 0 to n? 
    # Actually, the DP counts numbers with exactly 'cnt' bits set in the binary representation of length L,
    # but leading zeros are allowed in the DP (since we iterate digit 0 or 1).
    # However, the number 0 has 0 bits set. 
    # We are interested in positive integers x in [1, n].
    # The DP as written counts x in [0, n] (including 0) that have popcount in valid_c.
    # But note: the binary representation of x might have leading zeros in our DP, but the popcount is the same.
    # However, the number 0 is represented as all zeros, popcount=0.
    # We must exclude 0 if it is counted.
    # Also, we must ensure we are counting positive integers.
    # The DP counts all bit strings of length L that are <= n_bin, interpreted as numbers.
    # This includes 0 (all zeros).
    # So we compute total = dp(0, 0, True).
    # Then subtract 1 if 0 is counted (i.e., if 0 in valid_c). But 0 is not a positive integer, and our problem is about positive integers.
    # However, note that 0 is not in the range [1, n]. So we should subtract the count for 0.
    # But our DP counts 0 if pop[0]=0 is in valid_c.
    # So: total_positive = total - (1 if 0 in valid_c else 0).
    # But wait: is 0 ever in valid_c? 
    # valid_c contains c such that steps[c] == target.
    # steps[0] is not defined in our array (we started from 1). But logically, 0 has 0 bits, and reducing 0? 
    # The problem says positive integer x. So we don't consider 0.
    # So we must exclude 0 from our count.
    # How does the DP count 0? It counts the all-zero string.
    # So if 0 is in valid_c, we subtract 1. Otherwise, we don't.
    # But note: 0 is not a positive integer, so it shouldn't be counted anyway.
    # So: count = dp(0, 0, True) - (1 if 0 in valid_c else 0).
    
    # However, there's a catch: the DP counts numbers with leading zeros as having the same popcount, which is correct.
    # But the number 0 is the only one with popcount 0.
    # So if 0 in valid_c, we subtract 1.
    
    total = dp(0, 0, True)
    if 0 in valid_c:
        total = (total - 1 + MOD) % MOD
    
    # Now, if k >= 1, we must exclude x=1 if it was included.
    # x=1 has popcount=1. So if 1 in valid_c, then x=1 was counted.
    # But for k>=1, x=1 is not special (since ops(1)=0 != k).
    # So we subtract 1 if 1 in valid_c.
    
    if 1 in valid_c:
        total = (total - 1 + MOD) % MOD
    
    print(total)

if __name__ == '__main__':
    solve()