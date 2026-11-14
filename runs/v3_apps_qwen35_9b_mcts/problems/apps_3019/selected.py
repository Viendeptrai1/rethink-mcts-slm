import sys

def count_distinct_prime_factors(n):
    if n <= 1:
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

    # Precompute sums for all subsets
    # dp_sum[mask] = sum of S[i] for i in mask
    dp_sum = [0] * (1 << N)
    for mask in range(1, 1 << N):
        # Find the lowest set bit
        i = (mask & -mask).bit_length() - 1
        prev_mask = mask ^ (1 << i)
        dp_sum[mask] = dp_sum[prev_mask] + S[i]

    # Precompute revenue for each subset
    # rev[mask] = number of distinct prime factors of sum of subset
    rev = [0] * (1 << N)
    for mask in range(1, 1 << N):
        rev[mask] = count_distinct_prime_factors(dp_sum[mask])

    # DP for partitioning
    # dp[mask] = max revenue achievable using exactly the items in mask
    dp = [0] * (1 << N)
    
    # Base case: empty set has 0 revenue
    dp[0] = 0
    
    # Iterate through all masks
    for mask in range(1, 1 << N):
        # Try all submasks of mask as the first group
        # We iterate sub = mask, then sub = (sub - 1) & mask until 0
        sub = mask
        while True:
            # sub is a non-empty subset of mask
            remaining = mask ^ sub
            if dp[remaining] + rev[sub] > dp[mask]:
                dp[mask] = dp[remaining] + rev[sub]
            
            if sub == 0:
                break
            sub = (sub - 1) & mask

    print(dp[(1 << N) - 1])

if __name__ == "__main__":
    solve()