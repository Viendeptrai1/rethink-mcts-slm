import sys
from collections import defaultdict, deque

def find_spanning_tree_with_degree(n, m, D, edges):
    # Build adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Perform DFS to find a spanning tree
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
    
    # Check if we have a spanning tree
    if sum(visited) != n:
        return "NO"
    
    # Collect edges of the spanning tree
    spanning_tree_edges = []
    for v in range(2, n + 1):
        spanning_tree_edges.append((parent[v], v))
    
    # Count current degree of vertex 1
    current_degree = sum(1 for u, v in spanning_tree_edges if u == 1 or v == 1)
    
    # If the current degree is already D, we are done
    if current_degree == D:
        return "YES", spanning_tree_edges
    
    # If the current degree is less than D, we need to add more edges
    if current_degree < D:
        # Find leaves in the spanning tree
        leaves = [v for v in range(1, n + 1) if len(adj[v]) == 1 and v != 1]
        
        # Try to connect leaves to vertex 1
        added_edges = 0
        for leaf in leaves:
            if current_degree >= D:
                break
            if parent[leaf] != 1:
                spanning_tree_edges.append((1, leaf))
                current_degree += 1
                added_edges += 1
        
        # If we couldn't add enough edges, return "NO"
        if current_degree < D:
            return "NO"
    
    return "YES", spanning_tree_edges

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
D = int(data[2])
edges = [(int(data[3 + 2 * i]), int(data[4 + 2 * i])) for i in range(m)]

# Find spanning tree with required degree
result, spanning_tree_edges = find_spanning_tree_with_degree(n, m, D, edges)

# Print result
print(result)
if result == "YES":
    for u, v in spanning_tree_edges:
        print(u, v)