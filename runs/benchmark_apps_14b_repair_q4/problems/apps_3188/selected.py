import sys
import heapq

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    return data

def main():
    data = read_input()
    n = int(data[0])
    planets = []
    index = 1
    for _ in range(n):
        x = int(data[index])
        y = int(data[index + 1])
        z = int(data[index + 2])
        planets.append((x, y, z))
        index += 3
    
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            cost = min(abs(planets[i][0] - planets[j][0]), abs(planets[i][1] - planets[j][1]), abs(planets[i][2] - planets[j][2]))
            edges.append((cost, i, j))
    
    edges.sort()
    
    parent = list(range(n))
    rank = [0] * n
    
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
    
    mst_cost = 0
    edges_used = 0
    for cost, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            mst_cost += cost
            edges_used += 1
            if edges_used == n - 1:
                break
    
    print(mst_cost)

if __name__ == "__main__":
    main()