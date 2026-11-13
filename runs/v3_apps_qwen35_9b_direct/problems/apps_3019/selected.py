import sys

# Precompute the number of distinct prime factors for numbers up to 14 * 1000 = 14000
MAX_SUM = 14001
distinct_prime_factors = [0] * MAX_SUM

def count_distinct_prime_factors(n):
    if n < 2:
        return 0
    count = 0
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            count += 1
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        count += 1
    return count

# Precompute values
for i in range(2, MAX_SUM):
    distinct_prime_factors[i] = count_distinct_prime_factors(i)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        S = []
        for _ in range(N):
            S.append(int(next(iterator)))
    except StopIteration:
        return

    # dp[mask] = maximum revenue we can get from the subset of items represented by mask
    # We need to partition the full set (mask = (1<<N) - 1) into groups.
    # However, the standard approach for this specific problem (partitioning into subsets to maximize sum of f(sum))
    # is often solved by iterating over all possible submasks for the last group added.
    # But since N is small (<= 14), we can use a recursive DP with memoization or iterative DP.
    # Let dp[mask] be the max revenue for the subset 'mask'.
    # To compute dp[mask], we can iterate over all non-empty submasks 'sub' of 'mask'.
    # The last group sold is 'sub', and the remaining items are 'mask ^ sub'.
    # dp[mask] = max(dp[mask ^ sub] + distinct_prime_factors[sum(sub)]) for all sub in submasks(mask)
    
    # Optimization: Instead of iterating all submasks for every mask (which is O(3^N)), 
    # we can iterate masks from 1 to 2^N - 1.
    # For each mask, iterate over submasks. 3^14 is about 4.7 million, which is acceptable for Python if optimized.
    
    total_mask = (1 << N) - 1
    dp = [-1] * (1 << N)
    dp[0] = 0
    
    # Precompute sums for all masks to avoid recomputing
    mask_sums = [0] * (1 << N)
    for mask in range(1, 1 << N):
        # Find the lowest set bit
        lsb = mask & -mask
        idx = lsb.bit_length() - 1
        prev_mask = mask ^ lsb
        mask_sums[mask] = mask_sums[prev_mask] + S[idx]
    
    # Iterate through all masks
    for mask in range(1, 1 << N):
        # We want to find the best split: last group is 'sub', rest is 'mask ^ sub'
        # Iterate over all submasks of mask
        # Optimization: iterate only non-empty submasks
        sub = mask
        while sub > 0:
            # Calculate revenue for this split
            # dp[mask] = max(dp[mask], dp[mask ^ sub] + distinct_prime_factors[mask_sums[sub]])
            current_val = dp[mask ^ sub] + distinct_prime_factors[mask_sums[sub]]
            if current_val > dp[mask]:
                dp[mask] = current_val
            
            # Move to next submask: sub = (sub - 1) & mask
            sub = (sub - 1) & mask
    
    print(dp[total_mask])

if __name__ == '__main__':
    solve()