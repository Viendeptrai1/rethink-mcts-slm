MOD = 10**9 + 7

def count_arrangements(N, K):
    # Initialize the DP table
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    dp[0][0] = 1
    
    # Fill the DP table
    for n in range(1, N + 1):
        for k in range(K + 1):
            if k == 0:
                dp[n][k] = dp[n-1][k]
            else:
                dp[n][k] = (dp[n-1][k] + dp[n-1][k-1]) % MOD
                if n > k:
                    dp[n][k] = (dp[n][k] + dp[n-k-1][k-1]) % MOD
    
    # Extract the results for each i
    results = [dp[N][i] for i in range(1, K + 1)]
    
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])

# Get the results
results = count_arrangements(N, K)

# Print the results
for result in results:
    print(result)