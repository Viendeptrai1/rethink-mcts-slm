MOD = 10**9 + 7

def count_sequences(N, K):
    # Initialize the dp array
    dp = [[0] * (N + 1) for _ in range(K + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, N + 1):
        dp[1][j] = 1
    
    # Fill the dp array
    for i in range(2, K + 1):
        for j in range(1, N + 1):
            for k in range(1, N + 1):
                if k * j <= N:
                    dp[i][j] = (dp[i][j] + dp[i - 1][k]) % MOD
    
    # Sum up all sequences of length K
    result = sum(dp[K]) % MOD
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])

# Print the result
print(count_sequences(N, K))