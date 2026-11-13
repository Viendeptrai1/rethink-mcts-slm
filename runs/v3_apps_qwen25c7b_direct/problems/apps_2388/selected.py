MOD = 998244353

def count_remaining_robots(N, X, D):
    # Sort robots by their starting position
    robots = sorted(zip(X, D))
    
    # Initialize DP array where dp[i] represents the number of ways to leave robot i last
    dp = [0] * (N + 1)
    dp[0] = 1
    
    for i in range(1, N + 1):
        x, d = robots[i-1]
        # Calculate the farthest point any robot can reach
        farthest = x + d
        
        # Update DP array considering all previous robots
        for j in range(i-1, -1, -1):
            if robots[j][0] >= farthest:
                break
            dp[i] += dp[j]
            dp[i] %= MOD
    
    return sum(dp) % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
robots = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

# Output result
print(count_remaining_robots(N, [x for x, _ in robots], [d for _, d in robots]))