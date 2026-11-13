import sys
import heapq
from collections import defaultdict, deque

def shortest_paths_count(V, E, edges, s, t):
    # Create adjacency list
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    
    # Dijkstra's algorithm to find shortest path distances
    dist = [float('inf')] * V
    dist[s] = 0
    pq = [(0, s)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    # If the destination is unreachable
    if dist[t] == float('inf'):
        return 0
    
    # BFS to count shortest paths
    queue = deque([s])
    path_count = [0] * V
    path_count[s] = 1
    
    while queue:
        u = queue.popleft()
        for v, w in graph[u]:
            if dist[v] == dist[u] + w:
                path_count[v] += path_count[u]
                if path_count[v] == 1:  # First time visiting this node
                    queue.append(v)
    
    return path_count[t]

def main():
    input = sys.stdin.read
    data = input().split()
    
    V = int(data[0])
    E = int(data[1])
    
    edges = []
    index = 2
    for _ in range(E):
        u = int(data[index])
        v = int(data[index + 1])
        w = int(data[index + 2])
        edges.append((u, v, w))
        index += 3
    
    s = int(data[index])
    t = int(data[index + 1])
    
    result = shortest_paths_count(V, E, edges, s, t)
    print(result)

if __name__ == "__main__":
    main()