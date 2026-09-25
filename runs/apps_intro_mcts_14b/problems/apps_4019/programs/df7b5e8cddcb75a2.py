import sys
from collections import defaultdict, deque

def find_spanning_tree_with_degree(n, m, D, edges):
    # Build adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Check if it's possible to have a spanning tree with the required degree
    if D > n - 1:
        return "NO"
    
    # Try to construct a spanning tree with the required degree for vertex 1
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    degree = [0] * (n + 1)
    
    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                degree[u] += 1
                degree[v] += 1
                dfs(v)
    
    dfs(1)
    
    # If the degree of vertex 1 is already D, we can use the current spanning tree
    if degree[1] == D:
        result = []
        for v in range(2, n + 1):
            if parent[v] != -1:
                result.append((parent[v], v))
        return "YES", result
    
    # If the degree of vertex 1 is less than D, try to adjust the tree
    if degree[1] < D:
        # Find leaves in the current spanning tree
        leaves = [v for v in range(1, n + 1) if degree[v] == 1]
        
        # Try to connect more leaves to vertex 1
        while degree[1] < D and leaves:
            leaf = leaves.pop()
            if parent[leaf] != 1:
                # Remove the edge connecting the leaf to its parent
                degree[parent[leaf]] -= 1
                degree[leaf] -= 1
                
                # Connect the leaf directly to vertex 1
                parent[leaf] = 1
                degree[1] += 1
                degree[leaf] += 1
        
        # If we successfully increased the degree of vertex 1 to D
        if degree[1] == D:
            result = []
            for v in range(2, n + 1):
                if parent[v] != -1:
                    result.append((parent[v], v))
            return "YES", result
    
    return "NO"

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
D = int(data[2])
edges = [(int(data[3 + 2 * i]), int(data[4 + 2 * i])) for i in range(m)]

# Find and print the spanning tree
result = find_spanning_tree_with_degree(n, m, D, edges)
if result == "NO":
    print("NO")
else:
    print("YES")
    for u, v in result[1]:
        print(u, v)