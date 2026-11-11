import sys
import heapq
from collections import defaultdict

def count_shortest_paths(V, E, edges, s, t):
    # Build the graph
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    
    # Initialize distances and path counts
    dist = [float('inf')] * V
    path_count = [0] * V
    dist[s] = 0
    path_count[s] = 1
    
    # Min-heap to store (distance, vertex)
    heap = [(0, s)]
    
    while heap:
        current_dist, u = heapq.heappop(heap)
        
        if current_dist > dist[u]:
            continue
        
        for v, weight in graph[u]:
            new_dist = current_dist + weight
            
            if new_dist < dist[v]:
                dist[v] = new_dist
                path_count[v] = path_count[u]
                heapq.heappush(heap, (new_dist, v))
            elif new_dist == dist[v]:
                path_count[v] += path_count[u]
    
    return path_count[t]

# Read input
input = sys.stdin.read
data = input().split()
index = 0

V = int(data[index])
E = int(data[index + 1])
index += 2

edges = []
for _ in range(E):
    u = int(data[index])
    v = int(data[index + 1])
    w = int(data[index + 2])
    edges.append((u, v, w))
    index += 3

s = int(data[index])
t = int(data[index + 1])

# Calculate and print the number of different shortest paths
print(count_shortest_paths(V, E, edges, s, t))