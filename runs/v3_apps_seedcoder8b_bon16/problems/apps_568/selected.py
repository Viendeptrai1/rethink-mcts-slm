def count_ways(n):
    MOD = 10**9 + 7

    # The constraint a_i + a_{i+n} + a_{2n+i} ≠ 6 can be derived as:
    # a_i + a_{i+1} + a_{i+2} ≠ 6
    # Using this, we only need to count the valid distributions for a single triangle,
    # then raise to the power of 3n to account for all triangles.
    
    # Initialize a DP array where dp[k] represents the number of ways to distribute coins
    # in a single triangle such that the sum of coins on any of the three vertices is k.
    dp = [0] * 6
    dp[0] = 1  # There's one way to have zero coins on one vertex, two on another and none on the third.
    
    # Transition through possible distributions of coins
    for _ in range(n):
        new_dp = [0] * 6
        for sum_ in range(6):
            for coins in range(4):  # coins can be 0, 1, 2, or 3
                if sum_ + coins < 6:
                    new_dp[sum_ + coins] = (new_dp[sum_ + coins] + dp[sum_]) % MOD
        dp = new_dp
    
    # Count valid distributions
    valid_count = 0
    for sum_ in range(6):
        if (sum_ * 3) % 6 != 0:  # We want the sum of the three vertices to be a multiple of 2, i.e., not 6
            valid_count = (valid_count + dp[sum_]) % MOD
    
    # Raise the valid count to the power of 3n
    total_ways = pow(valid_count, n, MOD)
    
    return total_ways

# Read input
n = int(input().strip())

# Output the result
print(count_ways(n))