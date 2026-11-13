MOD = 10**9 + 7

def count_special_numbers(n_bin, k):
    n = int(n_bin, 2)
    
    # Precompute the number of set bits for all numbers up to n
    bit_count = [0] * (n + 1)
    for i in range(1, n + 1):
        bit_count[i] = bit_count[i >> 1] + (i & 1)
    
    # dp[i][j] will be the number of ways to reduce i to 1 using exactly j operations
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[1][0] = 1  # Base case: 1 can be reduced to 1 in 0 operations
    
    # Fill the dp table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            dp[i][j] = dp[bit_count[i]][j - 1]
    
    # Sum up all the ways to reduce numbers to 1 using exactly k operations
    result = sum(dp[i][k] for i in range(1, n + 1)) % MOD
    
    return result

# Read input
n_bin = input().strip()
k = int(input().strip())

# Compute and print the result
print(count_special_numbers(n_bin, k))