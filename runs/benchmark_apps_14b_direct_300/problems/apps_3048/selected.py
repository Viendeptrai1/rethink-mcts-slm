import sys
from collections import defaultdict, deque

def count_optimal_paths(N, edges):
    # Create adjacency list for the graph
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Function to perform BFS and find the shortest path lengths
    def bfs(start):
        queue = deque([(start, 0)])
        distances = {start: 0}
        while queue:
            node, dist = queue.popleft()
            for neighbor in adj_list[node]:
                if neighbor not in distances:
                    distances[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
        return distances
    
    # Calculate the number of optimal paths of length 2
    total_paths = 0
    for i in range(1, N + 1):
        distances = bfs(i)
        for j in range(1, N + 1):
            if i != j and distances[j] == 2:
                total_paths += 1
    
    return total_paths

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
edges = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N-1)]

# Calculate and print the result
result = count_optimal_paths(N, edges)
print(result)