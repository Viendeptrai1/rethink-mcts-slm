def minimal_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    # Initialize a list to mark blocked positions
    blocked = [False] * n
    for pos in blocked_positions:
        blocked[pos] = True

    # Initialize a list to store the minimum cost to illuminate up to each position
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # No cost to illuminate up to position 0

    # Iterate over each lamp power
    for power in range(1, k + 1):
        cost = lamp_costs[power - 1]
        # Iterate over each position to place the lamp
        for start in range(n):
            if blocked[start]:
                continue
            end = start + power
            if end > n:
                end = n
            # Update the dp array for the current lamp power
            for pos in range(start, end):
                dp[pos + 1] = min(dp[pos + 1], dp[start] + cost)

    # Check if the entire segment [0, n] is illuminated
    if dp[n] == float('inf'):
        return -1
    else:
        return dp[n]

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])
blocked_positions = list(map(int, data[3:3 + m]))
lamp_costs = list(map(int, data[3 + m:3 + m + k]))

# Get the result
result = minimal_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs)

# Print the result
print(result)