import sys
from collections import defaultdict, deque

def find_spanning_tree_with_degree(n, m, D, edges):
    # Build the adjacency list
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Check if it's possible to have a spanning tree with the required degree for vertex 1
    if D > n - 1:
        return "NO"
    
    # Perform BFS to find a spanning tree
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    queue = deque([1])
    visited[1] = True
    
    while queue:
        u = queue.popleft()
        for v in adj_list[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)
    
    # If we didn't visit all nodes, it means the graph is not connected
    if sum(visited) != n:
        return "NO"
    
    # Now we need to adjust the spanning tree to ensure the degree of vertex 1 is D
    # First, count the current degree of vertex 1
    current_degree = sum(1 for v in adj_list[1] if parent[v] == 1)
    
    # If the current degree is already D, we can return the spanning tree
    if current_degree == D:
        spanning_tree_edges = []
        for v in range(2, n + 1):
            if parent[v] != -1:
                spanning_tree_edges.append((parent[v], v))
        return "YES", spanning_tree_edges
    
    # Otherwise, we need to adjust the spanning tree
    # We will try to add or remove edges to achieve the desired degree
    if current_degree < D:
        # We need to add more edges
        available_edges = []
        for v in adj_list[1]:
            if parent[v] != 1:
                available_edges.append(v)
        
        if len(available_edges) < D - current_degree:
            return "NO"
        
        # Add the necessary edges
        added_edges = []
        for i in range(D - current_degree):
            v = available_edges[i]
            parent[v] = 1
            added_edges.append((1, v))
        
        # Now construct the spanning tree edges
        spanning_tree_edges = []
        for v in range(2, n + 1):
            if parent[v] != -1:
                spanning_tree_edges.append((parent[v], v))
        
        return "YES", spanning_tree_edges
    
    else:
        # We need to remove edges
        removable_edges = []
        for v in adj_list[1]:
            if parent[v] == 1:
                removable_edges.append(v)
        
        if len(removable_edges) < current_degree - D:
            return "NO"
        
        # Remove the unnecessary edges
        removed_edges = []
        for i in range(current_degree - D):
            v = removable_edges[i]
            parent[v] = -1
        
        # Now construct the spanning tree edges
        spanning_tree_edges = []
        for v in range(2, n + 1):
            if parent[v] != -1:
                spanning_tree_edges.append((parent[v], v))
        
        return "YES", spanning_tree_edges

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
D = int(data[2])
edges = [(int(data[3 + 2 * i]), int(data[4 + 2 * i])) for i in range(m)]

# Find the spanning tree
result, spanning_tree_edges = find_spanning_tree_with_degree(n, m, D, edges)

# Print the result
print(result)
if result == "YES":
    for u, v in spanning_tree_edges:
        print(u, v)