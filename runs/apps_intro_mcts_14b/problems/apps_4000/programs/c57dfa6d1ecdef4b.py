import sys
from collections import deque

def bfs(start, adj):
    queue = deque([start])
    dist = [-1] * len(adj)
    dist[start] = 0
    farthest_node = start
    max_dist = 0
    
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
                if dist[neighbor] > max_dist:
                    max_dist = dist[neighbor]
                    farthest_node = neighbor
    
    return farthest_node, max_dist, dist

def find_longest_path_tree(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)
    
    # First BFS to find one end of the diameter
    farthest_node1, _, _ = bfs(0, adj)
    
    # Second BFS to find the other end of the diameter
    farthest_node2, diameter, dist = bfs(farthest_node1, adj)
    
    # Find the farthest node from the second end of the diameter
    farthest_node3, _, _ = bfs(farthest_node2, adj)
    
    return farthest_node1 + 1, farthest_node2 + 1, farthest_node3 + 1, diameter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[i*2+1])-1, int(data[i*2+2])-1) for i in range(n-1)]
    
    a, b, c, res = find_longest_path_tree(n, edges)
    
    print(res)
    print(a, b, c)

if __name__ == "__main__":
    main()