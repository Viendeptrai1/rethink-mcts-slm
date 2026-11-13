import sys
from collections import defaultdict, deque

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    edges = []
    graph = defaultdict(list)
    
    index = 2
    for _ in range(m):
        u = int(data[index])
        v = int(data[index + 1])
        edges.append((u, v))
        graph[u].append(v)
        graph[v].append(u)
        index += 2
    
    # Check if the graph is a tree
    if m != n - 1:
        print("NO")
        return
    
    # Perform BFS to check for cycles and determine connectivity
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    
    def bfs(start):
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = node
                    queue.append(neighbor)
                elif parent[node] != neighbor:
                    # Found a back edge indicating a cycle
                    return False
        return True
    
    # Start BFS from any node (since the graph is connected)
    if not bfs(1):
        print("NO")
        return
    
    # If all nodes are visited, the graph is a tree
    print("YES")
    # Since the graph is a tree, we can orient the edges arbitrarily
    # Here we choose to orient edges from parent to child
    orientation = ['0'] * m
    for i, (u, v) in enumerate(edges):
        if parent[v] == u:
            orientation[i] = '1'
    
    print(''.join(orientation))

if __name__ == "__main__":
    main()