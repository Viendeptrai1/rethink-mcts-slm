import sys
import math

def min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    # Sort blocked positions for easier processing
    blocked_positions.sort()
    
    # Check if it's possible to illuminate the entire segment
    if m > 0 and (blocked_positions[0] == 0 or blocked_positions[-1] == n - 1):
        return -1
    
    # Initialize the minimum cost to infinity
    min_cost = float('inf')
    
    # Try each lamp power from 1 to k
    for l in range(1, k + 1):
        cost = lamp_costs[l - 1]
        num_lamps = 0
        current_position = 0
        
        while current_position < n:
            # Find the next position that is not blocked and can be illuminated by a lamp of power l
            next_position = current_position
            while next_position < n and (next_position in blocked_positions or next_position + l > n):
                next_position += 1
            
            # If we can't find a valid position, break
            if next_position >= n:
                break
            
            # Place a lamp at the found position
            num_lamps += 1
            current_position = next_position + l
        
        # Update the minimum cost if we successfully illuminated the entire segment
        if current_position >= n:
            min_cost = min(min_cost, num_lamps * cost)
    
    # If min_cost is still infinity, it means it's impossible to illuminate the entire segment
    if min_cost == float('inf'):
        return -1
    
    return min_cost

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

blocked_positions = list(map(int, data[3:3 + m]))
lamp_costs = list(map(int, data[3 + m:3 + m + k]))

# Output the result
print(min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs))