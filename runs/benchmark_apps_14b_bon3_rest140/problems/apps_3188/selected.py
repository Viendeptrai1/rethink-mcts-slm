import sys
import heapq

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    planets = []
    index = 1
    for i in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        z = int(data[index + 2])
        planets.append((x, y, z))
        index += 3
    
    return N, planets

def tunnel_cost(A, B):
    return min(abs(A[0] - B[0]), abs(A[1] - B[1]), abs(A[2] - B[2]))

def minimum_spanning_tree(N, planets):
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            cost = tunnel_cost(planets[i], planets[j])
            edges.append((cost, i, j))
    
    edges.sort()
    
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
    
    mst_cost = 0
    edge_count = 0
    for cost, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            mst_cost += cost
            edge_count += 1
            if edge_count == N - 1:
                break
    
    return mst_cost

def main():
    N, planets = read_input()
    result = minimum_spanning_tree(N, planets)
    print(result)

if __name__ == "__main__":
    main()