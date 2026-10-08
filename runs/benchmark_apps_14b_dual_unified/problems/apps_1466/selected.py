import sys
import heapq

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

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    k = int(data[index + 2])
    index += 3
    
    edges = [[] for _ in range(n + 1)]
    for _ in range(m):
        x = int(data[index])
        y = int(data[index + 1])
        w = int(data[index + 2])
        edges[x].append((y, w))
        edges[y].append((x, w))
        index += 3
    
    dist = dijkstra(n, edges, 1)
    
    edge_list = []
    for i in range(m):
        x = int(data[3 + i * 3])
        y = int(data[3 + i * 3 + 1])
        w = int(data[3 + i * 3 + 2])
        edge_list.append((w, i + 1, x, y))
    
    edge_list.sort()
    
    uf = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        if uf[x] != x:
            uf[x] = find(uf[x])
        return uf[x]
    
    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            if rank[rootX] > rank[rootY]:
                uf[rootY] = rootX
            elif rank[rootX] < rank[rootY]:
                uf[rootX] = rootY
            else:
                uf[rootY] = rootX
                rank[rootX] += 1
    
    remaining_edges = []
    for w, idx, x, y in edge_list:
        if find(x) != find(y):
            union(x, y)
            remaining_edges.append(idx)
            if len(remaining_edges) == k:
                break
    
    print(len(remaining_edges))
    print(*remaining_edges)

if __name__ == "__main__":
    main()