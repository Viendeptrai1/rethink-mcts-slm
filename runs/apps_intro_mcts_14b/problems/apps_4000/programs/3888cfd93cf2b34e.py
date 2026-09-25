import sys
from collections import deque

def bfs(start, graph):
    queue = deque([start])
    dist = [-1] * len(graph)
    dist[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

def find_diameter_and_farthest_node(graph):
    # First BFS to find one end of the diameter
    dist_from_0 = bfs(0, graph)
    farthest_node_1 = dist_from_0.index(max(dist_from_0))
    
    # Second BFS from the farthest node to find the other end of the diameter
    dist_from_farthest_1 = bfs(farthest_node_1, graph)
    farthest_node_2 = dist_from_farthest_1.index(max(dist_from_farthest_1))
    
    # Find the farthest node from the diameter's endpoints
    farthest_node_3 = max(range(len(graph)), key=lambda x: dist_from_farthest_1[x] + dist_from_0[x])
    
    return farthest_node_1, farthest_node_2, farthest_node_3, max(dist_from_farthest_1)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[2*i+1])-1, int(data[2*i+2])-1) for i in range(n-1)]
    
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    a, b, c, res = find_diameter_and_farthest_node(graph)
    
    print(res + 1)
    print(a + 1, b + 1, c + 1)

if __name__ == "__main__":
    main()