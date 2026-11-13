def minimal_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    # Initialize a list to mark blocked positions
    blocked = [False] * n
    for pos in blocked_positions:
        blocked[pos] = True

    # Initialize a list to store the minimum cost to illuminate up to each position
    min_cost = [float('inf')] * (n + 1)
    min_cost[0] = 0  # No cost to illuminate up to position 0

    # Iterate over each lamp power
    for power in range(1, k + 1):
        cost = lamp_costs[power - 1]
        # Traverse the street from right to left
        for i in range(n, -1, -1):
            if min_cost[i] == float('inf'):
                continue
            # Calculate the farthest position this lamp can illuminate
            farthest = min(n, i + power)
            # Update the minimum cost to illuminate up to the farthest position
            for j in range(i, farthest):
                if not blocked[j]:
                    min_cost[j + 1] = min(min_cost[j + 1], min_cost[i] + cost)

    # If the last position is still inf, it means it's not possible to illuminate the entire street
    return min_cost[n] if min_cost[n] != float('inf') else -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])
blocked_positions = list(map(int, data[3:3 + m]))
lamp_costs = list(map(int, data[3 + m:3 + m + k]))

# Get the result and print it
result = minimal_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs)
print(result)