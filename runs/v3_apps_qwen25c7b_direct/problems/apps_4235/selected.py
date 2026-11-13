def can_orient_graph(n, m, edges):
    # Check if the graph is a tree
    if m != n - 1:
        return "NO"
    
    # Create adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)
    
    # Perform DFS to check if the graph is a tree
    visited = [False] * n
    parent = [-1] * n
    
    def dfs(node, p):
        visited[node] = True
        parent[node] = p
        for neighbor in adj[node]:
            if not visited[neighbor]:
                if not dfs(neighbor, node):
                    return False
            elif neighbor != p:
                return False
        return True
    
    if not dfs(0, -1):
        return "NO"
    
    # Orient the edges
    orientation = ['0'] * m
    for i, (u, v) in enumerate(edges):
        if parent[u-1] == v-1:
            orientation[i] = '1'
    
    return "YES\n" + ''.join(orientation)

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
edges = [(int(data[2*i+2]), int(data[2*i+3])) for i in range(m)]

result = can_orient_graph(n, m, edges)
print(result)