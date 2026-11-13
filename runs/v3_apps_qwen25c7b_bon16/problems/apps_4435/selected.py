from collections import defaultdict, deque

def min_moves_to_opposite_parity(a):
    n = len(a)
    graph = defaultdict(list)
    
    # Create adjacency list for the graph
    for i in range(n):
        if i - a[i] >= 0:
            graph[i].append(i - a[i])
        if i + a[i] < n:
            graph[i].append(i + a[i])
    
    # Function to perform BFS and find the shortest distance to the opposite parity node
    def bfs(start):
        queue = deque([start])
        visited = set([start])
        distance = {start: 0}
        
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distance[neighbor] = distance[current] + 1
                    if a[neighbor] % 2 != a[start] % 2:
                        return distance[neighbor]
                    queue.append(neighbor)
        
        return -1
    
    # Calculate the result for each starting point
    result = [bfs(i) for i in range(n)]
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
a = list(map(int, data[1:]))

# Get the result
result = min_moves_to_opposite_parity(a)

# Print the result
print(' '.join(map(str, result)))