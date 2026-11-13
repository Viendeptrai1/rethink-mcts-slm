def min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    blocked_positions = set(blocked_positions)
    if 0 in blocked_positions or n - 1 in blocked_positions:
        return -1
    
    def can_cover(start, end, power):
        current = start
        while current <= end:
            next_pos = current + power
            if next_pos >= end:
                return True
            if next_pos in blocked_positions:
                next_pos += 1
            current = next_pos
        return False
    
    min_cost = float('inf')
    for power, cost in enumerate(lamp_costs, start=1):
        if can_cover(0, n - 1, power):
            min_cost = min(min_cost, cost * ((n - 1) // power + 1))
    
    return min_cost if min_cost != float('inf') else -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

blocked_positions = list(map(int, data[3:3+m]))
lamp_costs = list(map(int, data[3+m:]))

print(min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs))