import sys
from collections import defaultdict, deque

def find_spanning_tree_with_degree(n, m, D, edges):
    # Build adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Step 1: Perform DFS to find a spanning tree
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    stack = [1]
    visited[1] = True
    
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Step 2: Check if it's possible to adjust the degree of vertex 1 to D
    degree_1 = sum(1 for v in adj[1] if parent[v] == 1)
    if degree_1 > D:
        return "NO"
    
    # If degree_1 is already D, we can use the spanning tree found
    if degree_1 == D:
        spanning_tree = []
        for v in range(2, n + 1):
            if parent[v] != -1:
                spanning_tree.append((parent[v], v))
        return "YES", spanning_tree
    
    # Otherwise, we need to add more edges to increase the degree of vertex 1
    # We will try to add edges from vertex 1 to its children until the degree is D
    additional_edges = []
    for v in adj[1]:
        if parent[v] == 1:
            additional_edges.append(v)
    
    if len(additional_edges) + degree_1 < D:
        return "NO"
    
    # Add enough edges to make the degree of vertex 1 equal to D
    spanning_tree = []
    for v in range(2, n + 1):
        if parent[v] != -1:
            spanning_tree.append((parent[v], v))
    
    for i in range(D - degree_1):
        spanning_tree.append((1, additional_edges[i]))
    
    return "YES", spanning_tree

def main():
    import sys
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
    
    result, spanning_tree = find_spanning_tree_with_degree(n, m, D, edges)
    print(result)
    if result == "YES":
        for u, v in spanning_tree:
            print(u, v)

if __name__ == "__main__":
    main()