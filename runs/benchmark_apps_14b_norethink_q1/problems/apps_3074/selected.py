MOD = 10**9 + 7

def count_valid_subsets(N, S):
    # Initialize DP table
    dp = [[0] * 3 for _ in range(N + 1)]
    dp[0][0] = 1  # Base case: one way to have a sum of 0 with 0 elements

    for i in range(1, N + 1):
        digit = int(S[i - 1])
        for j in range(3):
            dp[i][j] = dp[i - 1][j]  # Exclude the current digit
            dp[i][j] += dp[i - 1][(j - digit) % 3]  # Include the current digit
            dp[i][j] %= MOD

    # Subtract 1 to exclude the empty subset
    return (dp[N][0] - 1) % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
S = data[1]

# Compute and print the result
result = count_valid_subsets(N, S)
print(result)