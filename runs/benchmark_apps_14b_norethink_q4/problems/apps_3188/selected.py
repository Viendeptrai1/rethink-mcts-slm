import sys
import heapq

def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)
    
    if rank[rootX] > rank[rootY]:
        parent[rootY] = rootX
    elif rank[rootX] < rank[rootY]:
        parent[rootX] = rootY
    else:
        parent[rootY] = rootX
        rank[rootX] += 1

def kruskalMST(points):
    n = len(points)
    edges = []
    
    for i in range(n):
        for j in range(i + 1, n):
            cost = min(abs(points[i][0] - points[j][0]), abs(points[i][1] - points[j][1]), abs(points[i][2] - points[j][2]))
            edges.append((cost, i, j))
    
    edges.sort()
    
    parent = list(range(n))
    rank = [0] * n
    
    mst_cost = 0
    edge_count = 0
    
    for cost, u, v in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_cost += cost
            edge_count += 1
            if edge_count == n - 1:
                break
    
    return mst_cost

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    
    points = []
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        z = int(data[index + 2])
        points.append((x, y, z))
        index += 3
    
    result = kruskalMST(points)
    print(result)

if __name__ == "__main__":
    main()