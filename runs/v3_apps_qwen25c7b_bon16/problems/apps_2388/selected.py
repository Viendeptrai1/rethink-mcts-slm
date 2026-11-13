MOD = 998244353

def count_remaining_sets(N, X, D):
    # Sort robots based on their starting position
    robots = sorted(zip(X, D))
    
    # Initialize DP array
    dp = [1] * N
    for i in range(1, N):
        for j in range(i):
            if robots[j][0] + robots[j][1] >= robots[i][0]:
                dp[i] += dp[j]
                dp[i] %= MOD
    
    # Calculate the total number of sets
    result = sum(dp) % MOD
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
robots = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

# Get the result
result = count_remaining_sets(N, [x for x, _ in robots], [d for _, d in robots])

# Output the result
print(result)