import sys
import heapq
from collections import defaultdict

def max_good_vertices(n, m, k, edges):
    # Build the graph
    graph = defaultdict(list)
    for idx, (x, y, w) in enumerate(edges, 1):
        graph[x].append((y, w, idx))
        graph[y].append((x, w, idx))
    
    # Dijkstra's algorithm to find shortest paths from vertex 1
    def dijkstra(source):
        dist = {i: float('inf') for i in range(1, n + 1)}
        dist[source] = 0
        priority_queue = [(0, source)]
        while priority_queue:
            current_dist, u = heapq.heappop(priority_queue)
            if current_dist > dist[u]:
                continue
            for v, weight, _ in graph[u]:
                distance = current_dist + weight
                if distance < dist[v]:
                    dist[v] = distance
                    heapq.heappush(priority_queue, (distance, v))
        return dist

    shortest_paths = dijkstra(1)
    
    # Extract edges sorted by weight
    edges_by_weight = sorted((w, x, y, i) for i, (x, y, w) in enumerate(edges, 1))
    
    # Use a union-find structure to keep track of connected components
    parent = list(range(n + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootY] = rootX
            return True
        return False
    
    remaining_edges = []
    for w, x, y, idx in edges_by_weight:
        if shortest_paths[x] + w == shortest_paths[y] or shortest_paths[y] + w == shortest_paths[x]:
            if union(x, y):
                remaining_edges.append(idx)
    
    # If we have more than k edges, we need to remove some
    if len(remaining_edges) > k:
        remaining_edges = remaining_edges[:k]
    
    # Output the result
    print(len(remaining_edges))
    print(' '.join(map(str, remaining_edges)))

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    edges = [(int(data[i * 3 + 3]), int(data[i * 3 + 4]), int(data[i * 3 + 5])) for i in range(m)]
    max_good_vertices(n, m, k, edges)