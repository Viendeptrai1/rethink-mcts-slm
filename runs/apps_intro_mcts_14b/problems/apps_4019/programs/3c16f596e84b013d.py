import sys
from typing import List, Tuple

def find(parent: List[int], i: int) -> int:
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent: List[int], rank: List[int], x: int, y: int) -> None:
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

def kruskal_with_degree_constraint(n: int, m: int, D: int, edges: List[Tuple[int, int]]) -> Tuple[bool, List[Tuple[int, int]]]:
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    degree = [0] * (n + 1)
    mst_edges = []
    
    # Sort edges by their presence in the original graph
    edges.sort(key=lambda x: (x[0] == 1 or x[1] == 1, x))
    
    for u, v in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_edges.append((u, v))
            degree[u] += 1
            degree[v] += 1
            
            # Check if the degree of vertex 1 is D
            if degree[1] == D:
                break
    
    # Check if we have a spanning tree
    if len(mst_edges) == n - 1:
        return True, mst_edges
    else:
        return False, []

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    D = int(data[index + 2])
    index += 3
    
    edges = []
    for _ in range(m):
        u = int(data[index])
        v = int(data[index + 1])
        edges.append((u, v))
        index += 2
    
    has_solution, mst_edges = kruskal_with_degree_constraint(n, m, D, edges)
    
    if has_solution:
        print("YES")
        for u, v in mst_edges:
            print(u, v)
    else:
        print("NO")

if __name__ == "__main__":
    main()