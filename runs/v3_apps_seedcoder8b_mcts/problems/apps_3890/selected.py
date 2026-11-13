def count_plaque_configurations(n, k):
    MOD = 1000000007

    # dp[i][j] will store the number of ways to configure the plaques such that
    # starting from house i, the penguin can reach house j after some walks.
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    # Base case: starting from house i, the penguin can reach house i after 0 walks.
    for i in range(1, n + 1):
        dp[i][i] = 1

    # Fill the dp table
    for length in range(1, n):
        for start in range(1, n - length + 1):
            end = start + length
            for mid in range(start, end):
                dp[start][end] = (dp[start][end] + dp[mid][end]) % MOD

    # Calculate the number of valid plaque configurations
    result = 0
    for i in range(1, k + 1):
        result = (result + dp[i][1]) % MOD

    for i in range(k + 1, n + 1):
        result = (result + dp[i][1]) % MOD

    return result

# Read input
import sys
input = sys.stdin.read
data = input().strip()
n, k = map(int, data.split())

# Output the result
print(count_plaque_configurations(n, k))