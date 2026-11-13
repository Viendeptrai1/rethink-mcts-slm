import sys
from heapq import heappop, heappush

def find_max_fee(N, P, X, Y, partnerships, swerc_banks):
    graph = [[] for _ in range(N + 1)]
    for a, b, c in partnerships:
        graph[a].append((b, c))
        graph[b].append((a, c))

    def dijkstra(start):
        dist = [float('inf')] * (N + 1)
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heappush(pq, (dist[v], v))
        return dist

    dist_x = dijkstra(X)
    dist_y = dijkstra(Y)

    max_fee = float('-inf')
    for a, b, c in partnerships:
        if a in swerc_banks and b in swerc_banks:
            if dist_x[a] + dist_y[b] == dist_x[Y]:
                max_fee = max(max_fee, c)

    if max_fee == float('-inf'):
        return "Impossible"
    elif max_fee == float('inf'):
        return "Infinity"
    else:
        return max_fee

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    P = int(data[index])
    index += 1
    X = int(data[index])
    index += 1
    Y = int(data[index])
    index += 1
    
    partnerships = []
    for _ in range(P):
        a = int(data[index])
        index += 1
        b = int(data[index])
        index += 1
        c = int(data[index])
        index += 1
        partnerships.append((a, b, c))
    
    M = int(data[index])
    index += 1
    swerc_banks = list(map(int, data[index:index + M]))
    index += M
    
    result = find_max_fee(N, P, X, Y, partnerships, swerc_banks)
    print(result)