import sys
from collections import defaultdict, deque

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    edges = []
    for i in range(m):
        u = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        edges.append((u, v))
    
    # Create adjacency list
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Check if the graph is a tree
    if m != n - 1:
        print("NO")
        return
    
    # Try to orient the edges
    orientation = [-1] * m
    visited = [False] * (n + 1)
    
    def dfs(node, parent):
        visited[node] = True
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                # Find the index of the edge (node, neighbor)
                edge_index = -1
                for i in range(m):
                    if (edges[i][0] == node and edges[i][1] == neighbor) or (edges[i][0] == neighbor and edges[i][1] == node):
                        edge_index = i
                        break
                if edge_index == -1:
                    continue
                
                # Orient the edge from node to neighbor
                orientation[edge_index] = 0
                if not dfs(neighbor, node):
                    return False
            elif neighbor != parent:
                # Found a back edge, which means we cannot avoid paths of length two
                return False
        return True
    
    # Start DFS from any node (e.g., node 1)
    if not dfs(1, -1):
        print("NO")
        return
    
    # If we reach here, it means we can orient the edges successfully
    print("YES")
    print("".join(map(str, orientation)))

if __name__ == "__main__":
    main()