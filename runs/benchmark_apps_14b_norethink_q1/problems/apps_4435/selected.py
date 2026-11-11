from collections import deque

def min_moves_to_opposite_parity(n, a):
    # Initialize the result list with -1
    result = [-1] * n
    
    # Helper function to check if two numbers have opposite parity
    def has_opposite_parity(x, y):
        return (x % 2) != (y % 2)
    
    # Perform BFS for each position
    for start in range(n):
        # If the result is already computed, skip
        if result[start] != -1:
            continue
        
        # Queue for BFS: stores tuples of (current_position, current_distance)
        queue = deque([(start, 0)])
        visited = set([start])
        
        while queue:
            current, distance = queue.popleft()
            
            # Check both possible jumps
            for next_pos in [current - a[current], current + a[current]]:
                # Check if the next position is within bounds
                if 0 <= next_pos < n:
                    # Check if the next position has opposite parity
                    if has_opposite_parity(a[current], a[next_pos]):
                        result[start] = distance + 1
                        break
                    # If not visited, add to the queue
                    if next_pos not in visited:
                        visited.add(next_pos)
                        queue.append((next_pos, distance + 1))
            
            # If we found a position with opposite parity, break out of the loop
            if result[start] != -1:
                break
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Get the result
result = min_moves_to_opposite_parity(n, a)

# Print the result
print(" ".join(map(str, result)))