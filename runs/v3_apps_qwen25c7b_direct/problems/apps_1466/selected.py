import heapq
from collections import defaultdict, deque

def dijkstra(graph, start):
    n = len(graph)
    dist = [float('inf')] * n
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

def find_min_edges_to_keep(n, edges, k):
    graph = defaultdict(list)
    for i, (x, y, w) in enumerate(edges, 1):
        graph[x-1].append((y-1, w))
        graph[y-1].append((x-1, w))
    
    initial_distances = dijkstra(graph, 0)
    
    # Sort edges by their weights
    sorted_edges = sorted(enumerate(edges), key=lambda x: x[1][2])
    
    remaining_edges = []
    removed_edges = set()
    
    for i, (x, y, w) in sorted_edges:
        if len(removed_edges) >= k:
            break
        
        # Check if removing this edge affects the shortest path to any vertex
        graph[x-1].remove((y-1, w))
        graph[y-1].remove((x-1, w))
        
        new_distances = dijkstra(graph, 0)
        
        if all(new_distances[i] == initial_distances[i] for i in range(n)):
            remaining_edges.append(i+1)
        else:
            removed_edges.add(i)
        
        graph[x-1].append((y-1, w))
        graph[y-1].append((x-1, w))
    
    return len(remaining_edges), remaining_edges

# Input reading
n, m, k = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

# Find the minimum number of edges to keep
result_count, result_edges = find_min_edges_to_keep(n, edges, k)

# Output the result
print(result_count)
print(*result_edges)