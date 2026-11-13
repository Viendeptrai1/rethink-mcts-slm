import sys
import math

# Precompute number of distinct prime factors for sums up to 14 * 1000 = 14000
MAX_SUM = 14000
prime_count = [0] * (MAX_SUM + 1)

def sieve_distinct_prime_counts():
    # Initialize with 0
    is_prime = [True] * (MAX_SUM + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, MAX_SUM + 1):
        if is_prime[i]:
            for j in range(i * i, MAX_SUM + 1, i):
                is_prime[j] = False
    
    # Count distinct prime factors for each number
    for i in range(2, MAX_SUM + 1):
        if is_prime[i]:
            for j in range(i, MAX_SUM + 1, i):
                prime_count[j] += 1

sieve_distinct_prime_counts()

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

    # Precompute values for all possible subsets of S
    # There are 2^N subsets. N <= 14, so 2^14 = 16384, which is small.
    # value[mask] = number of distinct prime factors of sum of elements in mask
    value = [0] * (1 << N)
    
    for mask in range(1, 1 << N):
        current_sum = 0
        for i in range(N):
            if mask & (1 << i):
                current_sum += S[i]
        value[mask] = prime_count[current_sum]
    
    # Use DP with bitmask to find maximum revenue
    # dp[mask] = max revenue for selling the subset of data represented by mask
    # We want dp[(1<<N) - 1]
    
    total_mask = (1 << N) - 1
    dp = [0] * (1 << N)
    
    # Base case: dp[0] = 0 is already set
    
    # Iterate through all masks
    for mask in range(1, total_mask + 1):
        # Try to form this mask by taking a submask 'sub' and selling the rest 'mask ^ sub' to one customer
        # Actually, the recurrence is:
        # dp[mask] = max over all submask 'sub' of 'mask' (where sub is non-empty and sub is a proper subset or the whole set)
        # of: dp[mask ^ sub] + value[sub]
        # But iterating over all submasks is O(3^N). 3^14 is about 4.7 million, which is acceptable in Python if optimized.
        
        best = 0
        
        # Optimization: iterate only over submasks of mask
        sub = mask
        while True:
            if sub != 0:
                # Calculate revenue if we sell 'sub' to one customer and the rest 'mask ^ sub' was already optimally sold
                # But wait, the problem says we partition the set into groups. Each group is sold to one customer.
                # The revenue for a group is value[group].
                # So dp[mask] = max( dp[mask ^ sub] + value[sub] ) for any non-empty sub of mask.
                # However, this recurrence considers the last group added as 'sub'.
                # Since addition is commutative, this covers all partitions.
                
                rev = dp[mask ^ sub] + value[sub]
                if rev > best:
                    best = rev
            
            # Remove the lowest set bit to iterate through submasks
            if sub == 0:
                break
            # sub = sub - (sub & -sub) is not correct for getting next submask in descending order easily without logic
            # Standard trick: sub = (sub - 1) & mask
            sub = (sub - 1) & mask
        
        dp[mask] = best

    print(dp[total_mask])

if __name__ == '__main__':
    solve()