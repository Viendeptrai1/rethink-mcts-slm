import sys
from typing import List

def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)

    if rootX != rootY:
        if rank[rootX] > rank[rootY]:
            parent[rootY] = rootX
        elif rank[rootX] < rank[rootY]:
            parent[rootX] = rootY
        else:
            parent[rootY] = rootX
            rank[rootX] += 1

def min_cost_to_connect_planets(N: int, planets: List[List[int]]) -> int:
    edges = []
    
    for i in range(N):
        for j in range(i + 1, N):
            dx = abs(planets[i][0] - planets[j][0])
            dy = abs(planets[i][1] - planets[j][1])
            dz = abs(planets[i][2] - planets[j][2])
            edges.append((min(dx, dy, dz), i, j))
    
    edges.sort()
    
    parent = list(range(N))
    rank = [0] * N
    
    mst_cost = 0
    num_edges = 0
    
    for weight, u, v in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_cost += weight
            num_edges += 1
            if num_edges == N - 1:
                break
    
    return mst_cost

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    planets = [[int(data[3*i+1]), int(data[3*i+2]), int(data[3*i+3])] for i in range(N)]
    
    result = min_cost_to_connect_planets(N, planets)
    print(result)