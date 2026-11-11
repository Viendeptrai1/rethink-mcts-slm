import sys
from itertools import combinations

def count_distinct_prime_factors(n):
    if n < 2:
        return 0
    count = 0
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            count += 1
            while n % factor == 0:
                n //= factor
        factor += 1
    if n > 1:
        count += 1
    return count

def max_revenue(N, S):
    # Initialize the dp array where dp[mask] is the maximum revenue for the subset of data pieces represented by mask
    dp = [0] * (1 << N)
    
    # Iterate over all subsets of data pieces
    for mask in range(1, 1 << N):
        # Calculate the sum of S_i for the current subset
        total_sum = sum(S[i] for i in range(N) if mask & (1 << i))
        # Calculate the number of distinct prime factors in the sum
        prime_factors_count = count_distinct_prime_factors(total_sum)
        # Update the dp value for the current subset
        dp[mask] = prime_factors_count
    
    # Now, we need to find the maximum revenue by considering all possible ways to partition the data
    max_revenue = 0
    for i in range(1, 1 << N):
        for j in range(i):
            if (i & j) == 0:  # i and j are disjoint sets
                max_revenue = max(max_revenue, dp[i] + dp[j])
    
    return max_revenue

if __name__ == "__main__":
    N = int(sys.stdin.readline().strip())
    S = list(map(int, sys.stdin.readline().strip().split()))
    print(max_revenue(N, S))