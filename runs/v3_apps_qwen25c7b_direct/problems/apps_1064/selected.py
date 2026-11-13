def min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    blocked = set(blocked_positions)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        if i in blocked:
            continue
        for j in range(1, k + 1):
            if i >= j:
                dp[i] = min(dp[i], dp[i - j] + lamp_costs[j - 1])
    
    return dp[n] if dp[n] != float('inf') else -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

blocked_positions = list(map(int, data[3:3+m]))
lamp_costs = list(map(int, data[3+m:]))

result = min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs)
print(result)