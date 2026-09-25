import sys
from collections import defaultdict, deque

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
        v = int(data[index])
        u = int(data[index + 1])
        edges.append((v, u))
        index += 2
    
    # Build adjacency list
    adj_list = defaultdict(list)
    for v, u in edges:
        adj_list[v].append(u)
        adj_list[u].append(v)
    
    # Check if the graph is already a tree
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    
    def bfs(start):
        queue = deque([start])
        visited[start] = True
        while queue:
            node = queue.popleft()
            for neighbor in adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = node
                    queue.append(neighbor)
                elif neighbor != parent[node]:
                    return False
        return True
    
    if not bfs(1):
        print("NO")
        return
    
    # Count the degree of the first vertex
    degree_1 = sum(1 for _ in adj_list[1])
    
    if degree_1 == D:
        # The graph is already a tree with the required degree for the first vertex
        print("YES")
        for v, u in edges:
            if parent[v] == u or parent[u] == v:
                print(v, u)
    else:
        # Try to modify the tree to meet the degree requirement
        if degree_1 > D:
            # Remove edges to reduce the degree of the first vertex
            to_remove = degree_1 - D
            removed_edges = []
            for neighbor in adj_list[1]:
                if parent[neighbor] == 1:
                    removed_edges.append((1, neighbor))
                    to_remove -= 1
                    if to_remove == 0:
                        break
            
            if len(removed_edges) != degree_1 - D:
                print("NO")
                return
            
            print("YES")
            for v, u in edges:
                if (v, u) not in removed_edges and (u, v) not in removed_edges:
                    print(v, u)
        else:
            # Add edges to increase the degree of the first vertex
            to_add = D - degree_1
            added_edges = []
            for neighbor in adj_list[1]:
                if parent[neighbor] == 1:
                    continue
                added_edges.append((1, neighbor))
                to_add -= 1
                if to_add == 0:
                    break
            
            if len(added_edges) != D - degree_1:
                print("NO")
                return
            
            print("YES")
            for v, u in edges:
                print(v, u)
            for v, u in added_edges:
                print(v, u)

if __name__ == "__main__":
    main()