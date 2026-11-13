import heapq
import sys
from collections import defaultdict, deque

def count_shortest_paths(V, E, edges, s, t):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    
    # Dijkstra's algorithm to find shortest path distances
    dist = [float('inf')] * V
    dist[s] = 0
    min_heap = [(0, s)]
    
    while min_heap:
        current_dist, u = heapq.heappop(min_heap)
        
        if current_dist > dist[u]:
            continue
        
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(min_heap, (dist[v], v))
    
    # If the destination is unreachable
    if dist[t] == float('inf'):
        return 0
    
    # BFS to count the number of shortest paths
    queue = deque([s])
    path_count = [0] * V
    path_count[s] = 1
    
    while queue:
        u = queue.popleft()
        
        for v, weight in graph[u]:
            if dist[v] == dist[u] + weight:
                if path_count[v] == 0:
                    queue.append(v)
                path_count[v] += path_count[u]
    
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
    
    result = count_shortest_paths(V, E, edges, s, t)
    print(result)

if __name__ == "__main__":
    main()