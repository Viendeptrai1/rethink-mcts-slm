import sys
import heapq

def min_tunnel_cost(N, planets):
    edges = []
    for i in range(N):
        for j in range(i+1, N):
            cost = min(abs(planets[i][k] - planets[j][k]) for k in range(3))
            heapq.heappush(edges, (cost, i, j))

    parent = list(range(N))
    rank = [0] * N

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True

    total_cost = 0
    edges_used = 0

    while edges and edges_used < N - 1:
        cost, u, v = heapq.heappop(edges)
        if union(u, v):
            total_cost += cost
            edges_used += 1

    return total_cost

def main():
    N = int(sys.stdin.readline())
    planets = [tuple(map(int, sys.stdin.readline().split())) for _ in range(N)]
    result = min_tunnel_cost(N, planets)
    print(result)

if __name__ == "__main__":
    main()