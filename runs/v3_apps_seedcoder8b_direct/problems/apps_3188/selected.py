import sys
import heapq

def find_minimum_tunnel_cost():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    planets = []
    
    index = 1
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        z = int(data[index + 2])
        planets.append((x, y, z))
        index += 3
    
    # Kruskal's algorithm requires sorting edges by weight
    edges = []
    
    # Generate all possible edges with their costs
    for i in range(N):
        for j in range(i + 1, N):
            x1, y1, z1 = planets[i]
            x2, y2, z2 = planets[j]
            cost = min(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))
            edges.append((cost, i, j))
    
    # Sort edges by cost
    edges.sort()
    
    # Union-Find (Disjoint Set Union) to manage connected components
    parent = list(range(N))
    rank = [0] * N
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        
        if rootX != rootY:
            if rank[rootX] > rank[rootY]:
                parent[rootY] = rootX
            elif rank[rootX] < rank[rootY]:
                parent[rootX] = rootY
            else:
                parent[rootY] = rootX
                rank[rootX] += 1
            return True
        return False
    
    # Kruskal's algorithm to find the Minimum Spanning Tree (MST)
    mst_cost = 0
    edges_used = 0
    
    for cost, u, v in edges:
        if union(u, v):
            mst_cost += cost
            edges_used += 1
            if edges_used == N - 1:
                break
    
    print(mst_cost)