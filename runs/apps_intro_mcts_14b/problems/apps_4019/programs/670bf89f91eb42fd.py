import sys
from collections import defaultdict, deque

def find_spanning_tree_with_degree(n, m, D, edges):
    # Build the adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Check if the graph is already a tree
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    
    def dfs(node, par):
        visited[node] = True
        parent[node] = par
        for neighbor in adj[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif neighbor != par:
                return True
        return False
    
    if dfs(1, -1):
        return "NO"
    
    # Count the degree of the first vertex
    degree_1 = sum(1 for _ in adj[1])
    
    # If the degree of the first vertex is already D, we can return the original edges
    if degree_1 == D:
        return "YES\n" + "\n".join(f"{u} {v}" for u, v in edges)
    
    # If the degree of the first vertex is less than D, we need to add more edges
    if degree_1 < D:
        additional_edges = []
        for v in range(2, n + 1):
            if len(adj[v]) < n - 1:
                additional_edges.append((1, v))
                adj[1].append(v)
                adj[v].append(1)
                degree_1 += 1
                if degree_1 == D:
                    break
        
        if degree_1 != D:
            return "NO"
        
        # Ensure the rest forms a tree
        visited = [False] * (n + 1)
        visited[1] = True
        queue = deque([1])
        tree_edges = set()
        
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    tree_edges.add((min(node, neighbor), max(node, neighbor)))
                    queue.append(neighbor)
        
        if len(tree_edges) != n - 1:
            return "NO"
        
        return "YES\n" + "\n".join(f"{u} {v}" for u, v in tree_edges | set(additional_edges))
    
    # If the degree of the first vertex is greater than D, we need to remove edges
    if degree_1 > D:
        removed_edges = []
        for v in adj[1]:
            if len(adj[v]) > 1:
                removed_edges.append((1, v))
                adj[1].remove(v)
                adj[v].remove(1)
                degree_1 -= 1
                if degree_1 == D:
                    break
        
        if degree_1 != D:
            return "NO"
        
        # Ensure the rest forms a tree
        visited = [False] * (n + 1)
        visited[1] = True
        queue = deque([1])
        tree_edges = set()
        
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    tree_edges.add((min(node, neighbor), max(node, neighbor)))
                    queue.append(neighbor)
        
        if len(tree_edges) != n - 1:
            return "NO"
        
        return "YES\n" + "\n".join(f"{u} {v}" for u, v in tree_edges)
    
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
print(result)