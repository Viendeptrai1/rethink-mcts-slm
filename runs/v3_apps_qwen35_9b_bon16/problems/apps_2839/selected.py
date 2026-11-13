import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        V = int(next(iterator))
        E = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(V)]
    
    for _ in range(E):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        adj[u].append((v, w))
    
    try:
        s = int(next(iterator))
        t = int(next(iterator))
    except StopIteration:
        return

    if s == t:
        print(1)
        return

    # Dijkstra's algorithm to find shortest distances and count paths
    INF = float('inf')
    dist = [INF] * V
    count = [0] * V
    dist[s] = 0
    count[s] = 1
    
    # Priority queue: (distance, vertex)
    pq = [(0, s)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, w in adj[u]:
            new_dist = dist[u] + w
            
            if new_dist < dist[v]:
                dist[v] = new_dist
                count[v] = count[u]
                heapq.heappush(pq, (new_dist, v))
            elif new_dist == dist[v]:
                count[v] += count[u]
                
    if dist[t] == INF:
        print(0)
    else:
        print(count[t])

import heapq

if __name__ == "__main__":
    solve()