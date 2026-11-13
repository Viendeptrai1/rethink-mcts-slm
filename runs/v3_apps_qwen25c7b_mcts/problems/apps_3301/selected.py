import sys
from heapq import heappop, heappush

def dijkstra(n, edges, start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        d, u = heappop(pq)
        if d > dist[u]:
            continue
        for v, w in edges[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heappush(pq, (dist[v], v))
    
    return dist

def find_max_fee(N, P, X, Y, edges, M, swerc_banks):
    max_fee = float('inf')
    min_dist = dijkstra(N, edges, X)[Y]
    
    for fee in range(1, 1000000001):
        modified_edges = {u: [] for u in range(1, N + 1)}
        for u, v, w in edges.values():
            if u in swerc_banks and v in swerc_banks:
                modified_edges[u].append((v, w + fee))
                modified_edges[v].append((u, w + fee))
        
        new_min_dist = dijkstra(N, modified_edges, X)[Y]
        if new_min_dist == min_dist:
            max_fee = fee
    
    return max_fee if max_fee != float('inf') else 'Impossible'

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    P = int(data[index + 1])
    X = int(data[index + 2])
    Y = int(data[index + 3])
    index += 4
    
    edges = {}
    for _ in range(P):
        a = int(data[index])
        b = int(data[index + 1])
        c = int(data[index + 2])
        index += 3
        
        if a not in edges:
            edges[a] = []
        if b not in edges:
            edges[b] = []
        
        edges[a].append((b, c))
        edges[b].append((a, c))
    
    M = int(data[index])
    index += 1
    swerc_banks = list(map(int, data[index:index + M]))
    
    result = find_max_fee(N, P, X, Y, edges, M, swerc_banks)
    print(result)