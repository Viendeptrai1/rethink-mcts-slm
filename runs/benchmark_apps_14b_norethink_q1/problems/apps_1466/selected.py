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
    
    if rootX != rootY:
        if rank[rootX] > rank[rootY]:
            parent[rootY] = rootX
        elif rank[rootX] < rank[rootY]:
            parent[rootX] = rootY
        else:
            parent[rootY] = rootX
            rank[rootX] += 1

def max_good_vertices(n, m, k, edges):
    # Step 1: Build the MST using Kruskal's algorithm
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    mst_edges = []
    edges.sort(key=lambda x: x[2])
    
    for u, v, w in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_edges.append((u, v, w))
    
    # Step 2: Add back edges to reach the desired number of edges (k)
    remaining_edges = k - len(mst_edges)
    added_edges = []
    
    for u, v, w in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            added_edges.append((u, v, w))
            remaining_edges -= 1
            if remaining_edges == 0:
                break
    
    # Step 3: Collect the indices of the edges in the final graph
    edge_indices = {edge: idx + 1 for idx, edge in enumerate(edges)}
    result_edges = mst_edges + added_edges
    result_edge_indices = [edge_indices[edge] for edge in result_edges]
    
    return len(result_edges), result_edge_indices

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
k = int(data[2])
edges = []

for i in range(m):
    x = int(data[3 + 3 * i])
    y = int(data[4 + 3 * i])
    w = int(data[5 + 3 * i])
    edges.append((x, y, w))

# Solve the problem
e, edge_indices = max_good_vertices(n, m, k, edges)

# Print the result
print(e)
print(" ".join(map(str, edge_indices)))