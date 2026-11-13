import heapq
from collections import defaultdict

def dijkstra(V, E, edges, s, t):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    
    dist = [float('inf')] * V
    dist[s] = 0
    pq = [(0, s)]
    num_paths = [0] * V
    num_paths[s] = 1
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > dist[u]:
            continue
        
        for v, w in graph[u]:
            distance = current_dist + w
            
            if distance < dist[v]:
                dist[v] = distance
                num_paths[v] = num_paths[u]
                heapq.heappush(pq, (distance, v))
            elif distance == dist[v]:
                num_paths[v] += num_paths[u]
    
    return num_paths[t]

# Read input
V, E = map(int, input().split())
edges = []
for _ in range(E):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))
s, t = map(int, input().split())

# Calculate and print the number of different shortest paths
print(dijkstra(V, E, edges, s, t))