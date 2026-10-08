import sys

def min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    # Sort blocked positions for easier processing
    blocked_positions.sort()
    
    # Function to check if a given lamp power can illuminate the entire segment
    def can_illuminate(power):
        last_illuminated = -1
        i = 0
        while i < n:
            if i in blocked_positions:
                i += 1
                continue
            if i <= last_illuminated:
                i += 1
                continue
            # Find the farthest point we can illuminate from position i
            farthest = min(i + power - 1, n - 1)
            # Move to the next position after the farthest illuminated point
            while i <= farthest:
                if i in blocked_positions:
                    break
                i += 1
            last_illuminated = farthest
        return i >= n
    
    # Initialize the minimum cost to a large number
    min_cost = float('inf')
    best_power = -1
    
    # Iterate over each possible lamp power
    for power in range(1, k + 1):
        if can_illuminate(power):
            cost = (n // power) * lamp_costs[power - 1]
            if n % power != 0:
                cost += lamp_costs[power - 1]
            if cost < min_cost:
                min_cost = cost
                best_power = power
    
    if best_power == -1:
        return -1
    else:
        return min_cost

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

blocked_positions = list(map(int, data[3:3 + m]))
lamp_costs = list(map(int, data[3 + m:]))

# Output the result
print(min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs))