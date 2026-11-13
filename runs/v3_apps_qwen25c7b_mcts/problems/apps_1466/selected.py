import heapq
from collections import defaultdict

def dijkstra(n, edges, start):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v, weight in graph[u]:
            distance = current_dist + weight
            if distance < dist[v]:
                dist[v] = distance
                heapq.heappush(pq, (distance, v))
    
    return dist

def max_good_vertices(n, m, k, edges):
    dist = dijkstra(n, edges, 1)
    good_edges = set()
    for i in range(1, n + 1):
        if dist[i] != float('inf'):
            good_edges.add(i)
    
    remaining_edges = []
    for i, (u, v, w) in enumerate(edges, 1):
        if u in good_edges and v in good_edges:
            remaining_edges.append(i)
    
    remaining_edges.sort(key=lambda x: edges[x-1][2])
    selected_edges = remaining_edges[:min(k, len(remaining_edges))]
    
    return len(selected_edges), selected_edges

# Input reading
n, m, k = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

# Output
result = max_good_vertices(n, m, k, edges)
print(result[0])
for edge in result[1]:
    print(edge, end=' ')