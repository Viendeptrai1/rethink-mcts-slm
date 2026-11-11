import sys

def max_monsters_defeated(N, A, B):
    # Initialize DP table
    dp = [0] * (N + 2)
    
    # Fill the DP table
    for i in range(1, N + 1):
        dp[i] = max(dp[i], dp[i - 1])  # Option 1: Hero i does not help
        dp[i + 1] = max(dp[i + 1], dp[i - 1] + min(A[i], B[i]))  # Option 2: Hero i helps town i
        dp[i + 1] = max(dp[i + 1], dp[i] + min(A[i + 1], B[i]))  # Option 3: Hero i helps town i+1
    
    return dp[N + 1]

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N + 2]))
B = list(map(int, data[N + 2:]))

# Calculate and print the result
result = max_monsters_defeated(N, A, B)
print(result)