MOD = 998244353

def count_remaining_robots(N, robots):
    # Sort robots by their starting position
    robots.sort()
    
    # Initialize DP array
    dp = [0] * (N + 1)
    dp[0] = 1
    
    # Iterate over each robot
    for i in range(1, N + 1):
        x, d = robots[i - 1]
        # Update DP array in reverse order to avoid overwriting
        for j in range(i - 1, -1, -1):
            if robots[j][0] + robots[j][1] > x:
                dp[j] = (dp[j] + dp[j + 1]) % MOD
        dp[i] = dp[i - 1]
    
    # Sum up all possible states where some robots remain
    result = sum(dp[:N]) % MOD
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
robots = []
index = 1
for i in range(N):
    x = int(data[index])
    d = int(data[index + 1])
    robots.append((x, d))
    index += 2

# Print the result
print(count_remaining_robots(N, robots))