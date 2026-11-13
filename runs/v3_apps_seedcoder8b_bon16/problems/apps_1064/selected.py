def min_cost_to_illuminate_street(n, m, k, blocked_positions, costs):
    # Initialize a DP array where dp[i] represents the minimal cost to illuminate [0, i]
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case: no cost to illuminate [0, 0]

    # A set for blocked positions for quick lookup
    blocked_set = set(blocked_positions)

    # Iterate over each possible end position for the street segment
    for i in range(1, n + 1):
        if i in blocked_set:
            continue  # Skip blocked positions

        # Iterate over each lamp power and calculate the possible illumination
        for power in range(1, k + 1):
            start_position = max(0, i - power)
            if start_position in blocked_set:
                continue  # Lamp start position can't be blocked

            # Update dp[i] based on the cost to place a lamp at `start_position`
            dp[i] = min(dp[i], dp[start_position] + costs[power - 1])

    # Check if we were able to illuminate the entire segment [0, n]
    return dp[n] if dp[n] != float('inf') else -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

blocked_positions = list(map(int, data[3:3 + m]))
costs = list(map(int, data[3 + m:3 + m + k]))

# Output the result
print(min_cost_to_illuminate_street(n, m, k, blocked_positions, costs))