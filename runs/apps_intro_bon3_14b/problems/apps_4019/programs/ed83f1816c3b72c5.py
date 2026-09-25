import sys
from collections import defaultdict, deque

def find_spanning_tree(n, m, D, edges):
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
    
    # Count the degree of vertex 1 in the spanning tree
    degree_1 = sum(1 for v in adj_list[1] if parent[v] == 1)
    
    # If the degree of vertex 1 is already D, we can return the spanning tree
    if degree_1 == D:
        spanning_tree_edges = []
        for v in range(2, n + 1):
            if parent[v] != -1:
                spanning_tree_edges.append((parent[v], v))
        return "YES\n" + "\n".join(f"{u} {v}" for u, v in spanning_tree_edges)
    
    # Otherwise, we need to adjust the spanning tree
    # Find a leaf node that is not adjacent to vertex 1
    leaf_node = None
    for v in range(2, n + 1):
        if len(adj_list[v]) == 1 and parent[v] != 1:
            leaf_node = v
            break
    
    if leaf_node is None:
        return "NO"
    
    # Remove the edge from the leaf node to its parent
    spanning_tree_edges = []
    for v in range(2, n + 1):
        if parent[v] != -1:
            spanning_tree_edges.append((parent[v], v))
    
    # Add an edge between vertex 1 and the leaf node
    spanning_tree_edges.append((1, leaf_node))
    
    # Adjust the degree of vertex 1
    degree_1 += 1
    
    # If the degree of vertex 1 is still not D, we need to remove some edges
    if degree_1 > D:
        extra_edges = degree_1 - D
        removed_edges = []
        for v in adj_list[1]:
            if parent[v] == 1:
                removed_edges.append((1, v))
                extra_edges -= 1
                if extra_edges == 0:
                    break
        
        # Remove the extra edges from the spanning tree
        spanning_tree_edges = [e for e in spanning_tree_edges if e not in removed_edges]
    
    return "YES\n" + "\n".join(f"{u} {v}" for u, v in spanning_tree_edges)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
D = int(data[2])
edges = [(int(data[3 + 2 * i]), int(data[4 + 2 * i])) for i in range(m)]

# Find and print the spanning tree
result = find_spanning_tree(n, m, D, edges)
print(result)