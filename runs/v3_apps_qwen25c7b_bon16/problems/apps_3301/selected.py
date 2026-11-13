import heapq

def find_largest_fee(N, P, X, Y, partnerships, swerc_banks):
    graph = [[] for _ in range(N + 1)]
    for a, b, c in partnerships:
        graph[a].append((b, c))
        graph[b].append((a, c))

    def dijkstra(start):
        dist = [float('inf')] * (N + 1)
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

    dist_x = dijkstra(X)
    dist_y = dijkstra(Y)

    max_fee = -1
    for u in swerc_banks:
        if u == X or u == Y:
            continue
        min_dist = float('inf')
        for v in range(1, N + 1):
            if v == X or v == Y or v == u:
                continue
            if dist_x[v] != float('inf') and dist_y[v] != float('inf'):
                min_dist = min(min_dist, dist_x[v] + dist_y[v])
        if min_dist != float('inf'):
            max_fee = max(max_fee, min_dist - dist_x[u] - dist_y[u])

    if max_fee == -1:
        return 'Impossible'
    elif max_fee == float('inf'):
        return 'Infinity'
    else:
        return max_fee

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
P = int(data[1])
X = int(data[2])
Y = int(data[3])
partnerships = []
index = 4
for _ in range(P):
    a = int(data[index])
    b = int(data[index + 1])
    c = int(data[index + 2])
    partnerships.append((a, b, c))
    index += 3

M = int(data[index])
swerc_banks = list(map(int, data[index + 1:]))

# Compute and print the result
print(find_largest_fee(N, P, X, Y, partnerships, swerc_banks))