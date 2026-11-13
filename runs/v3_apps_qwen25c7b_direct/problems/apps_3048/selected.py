from collections import defaultdict

def count_optimal_paths(N, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    total_paths = 0
    
    for node in range(1, N + 1):
        neighbors = set(graph[node])
        for neighbor in neighbors:
            for next_neighbor in neighbors:
                if next_neighbor != neighbor and next_neighbor in graph[neighbor]:
                    total_paths += 1
    
    return total_paths

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
edges = [(int(data[i * 2 + 1]), int(data[i * 2 + 2])) for i in range(N - 1)]

# Calculate and print the result
print(count_optimal_paths(N, edges))