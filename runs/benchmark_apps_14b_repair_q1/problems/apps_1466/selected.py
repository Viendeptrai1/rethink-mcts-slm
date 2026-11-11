import heapq
from collections import defaultdict

def dijkstra(n, edges, start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in edges[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist

def find_critical_edges(n, edges, dist):
    critical_edges = set()
    for u in range(1, n + 1):
        for v, w in edges[u]:
            if dist[u] + w == dist[v]:
                critical_edges.add((u, v))
                critical_edges.add((v, u))
    return critical_edges

def max_good_vertices(n, m, k, edges):
    # Step 1: Calculate shortest paths from vertex 1
    dist = dijkstra(n, edges, 1)
    
    # Step 2: Find critical edges
    critical_edges = find_critical_edges(n, edges, dist)
    
    # Step 3: Select up to k edges to retain
    selected_edges = []
    edge_list = list(edges.items())
    for i, (u, neighbors) in enumerate(edge_list):
        for v, w in neighbors:
            if (u, v) in critical_edges or (v, u) in critical_edges:
                selected_edges.append(i + 1)
                if len(selected_edges) == k:
                    break
        if len(selected_edges) == k:
            break
    
    # Output the result
    print(len(selected_edges))
    print(*selected_edges)

# Read input
n, m, k = map(int, input().split())
edges = defaultdict(list)
for i in range(m):
    x, y, w = map(int, input().split())
    edges[x].append((y, w))
    edges[y].append((x, w))

# Solve the problem
max_good_vertices(n, m, k, edges)