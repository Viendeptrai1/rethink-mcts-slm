import sys

def min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    def can_illuminate_with_power(power):
        count = 0
        current_position = 0
        blocked_set = set(blocked_positions)
        
        while current_position < n:
            if current_position in blocked_set:
                return float('inf')
            
            # Move to the next position that is not blocked and can be illuminated
            next_position = current_position + power
            while next_position < n and next_position not in blocked_set:
                next_position += power
            
            count += 1
            current_position = next_position
        
        return count
    
    min_cost = float('inf')
    
    for power in range(1, k + 1):
        num_lamps = can_illuminate_with_power(power)
        if num_lamps != float('inf'):
            min_cost = min(min_cost, num_lamps * lamp_costs[power - 1])
    
    return min_cost if min_cost != float('inf') else -1

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

blocked_positions = list(map(int, data[3:3 + m]))
lamp_costs = list(map(int, data[3 + m:3 + m + k]))

# Calculate and print the result
result = min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs)
print(result)