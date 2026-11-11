import sys
import heapq

def min_cost_to_connect_planets(N, planets):
    # Create a list of edges with their costs
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            cost = min(abs(planets[i][0] - planets[j][0]), abs(planets[i][1] - planets[j][1]), abs(planets[i][2] - planets[j][2]))
            edges.append((cost, i, j))
    
    # Sort edges by cost
    edges.sort()
    
    # Initialize union-find data structure
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
    
    # Kruskal's algorithm to find the minimum spanning tree
    min_cost = 0
    edges_used = 0
    for cost, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            min_cost += cost
            edges_used += 1
            if edges_used == N - 1:
                break
    
    return min_cost

# Read input
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

# Calculate and print the minimum cost
print(min_cost_to_connect_planets(N, planets))