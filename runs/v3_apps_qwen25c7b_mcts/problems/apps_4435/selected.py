from collections import deque
import sys

def min_moves_to_opposite_parity(n, a):
    # Create adjacency list for the graph
    graph = [[] for _ in range(n)]
    
    # Build the graph with valid jumps
    for i in range(n):
        if i - a[i] >= 0:
            graph[i].append(i - a[i])
        if i + a[i] < n:
            graph[i].append(i + a[i])
    
    # Initialize results array with -1
    results = [-1] * n
    
    # Perform BFS for each position
    for start in range(n):
        if results[start] != -1:
            continue
        
        queue = deque([start])
        visited = set([start])
        distance = 0
        
        while queue:
            size = len(queue)
            for _ in range(size):
                current = queue.popleft()
                
                # Check if we reached a position with opposite parity
                if a[current] % 2 != a[start] % 2:
                    results[start] = distance
                    break
                
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            if results[start] != -1:
                break
            
            distance += 1
    
    return results

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Get results
results = min_moves_to_opposite_parity(n, a)

# Print results
print(" ".join(map(str, results)))