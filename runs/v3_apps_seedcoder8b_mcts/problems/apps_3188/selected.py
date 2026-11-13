import sys
import heapq

def find(parent, i):
    if parent[i] == i:
        return i
    else:
        return find(parent, parent[i])

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

def kruskal_mst(N, edges):
    result = []
    i, e = 0, 0
    edges = sorted(edges, key=lambda item: item[2])
    parent = []
    rank = []
    
    for node in range(N):
        parent.append(node)
        rank.append(0)
    
    while e < N - 1:
        u, v, w = edges[i]
        i += 1
        x = find(parent, u)
        y = find(parent, v)
        
        if x != y:
            e += 1
            result.append(w)
            union(parent, rank, x, y)
    
    return sum(result)

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    coordinates = []
    
    index = 1
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        z = int(data[index + 2])
        coordinates.append((x, y, z))
        index += 3
    
    edges = []
    
    for i in range(N):
        for j in range(i + 1, N):
            cost = min(abs(coordinates[i][0] - coordinates[j][0]),
                       abs(coordinates[i][1] - coordinates[j][1]),
                       abs(coordinates[i][2] - coordinates[j][2]))
            edges.append((i, j, cost))
    
    min_cost = kruskal_mst(N, edges)
    print(min_cost)

if __name__ == "__main__":
    main()