import sys
from collections import deque

def min_moves_to_opposite_parity(n, a):
    # Initialize the result list with -1
    result = [-1] * n
    
    # Function to perform BFS from a given start index
    def bfs(start):
        queue = deque([(start, 0)])  # (current_index, current_distance)
        visited = set([start])
        
        while queue:
            current_index, distance = queue.popleft()
            
            # Check both possible jumps
            for next_index in [current_index - a[current_index], current_index + a[current_index]]:
                if 1 <= next_index <= n and next_index not in visited:
                    visited.add(next_index)
                    queue.append((next_index, distance + 1))
                    
                    # If we find a position with opposite parity, update the result and stop BFS
                    if a[next_index] % 2 != a[start] % 2:
                        result[start] = distance + 1
                        return
    
    # Perform BFS from each position
    for i in range(n):
        if result[i] == -1:  # Only perform BFS if the result is still -1
            bfs(i)
    
    return result

# Read input
n = int(sys.stdin.readline().strip())
a = list(map(int, sys.stdin.readline().strip().split()))

# Get the result
result = min_moves_to_opposite_parity(n, a)

# Print the result
print(" ".join(map(str, result)))