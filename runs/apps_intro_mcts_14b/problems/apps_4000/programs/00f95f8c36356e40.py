import sys
from collections import deque

def bfs(start, graph):
    dist = [-1] * len(graph)
    queue = deque([start])
    dist[start] = 0
    max_dist = 0
    farthest_node = start
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
                if dist[neighbor] > max_dist:
                    max_dist = dist[neighbor]
                    farthest_node = neighbor
    
    return farthest_node, max_dist, dist

def find_diameter_and_path_ends(graph):
    # Find the farthest node from an arbitrary starting node (node 0)
    _, _, dist_from_0 = bfs(0, graph)
    
    # Find the farthest node from the farthest node found in the previous step
    farthest_node, diameter, _ = bfs(dist_from_0.index(max(dist_from_0)), graph)
    
    return farthest_node, diameter

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
    
    # Find the diameter and the two endpoints of the diameter
    farthest_node, diameter = find_diameter_and_path_ends(graph)
    
    # The two endpoints of the diameter are the farthest nodes
    a, b = farthest_node, dist_from_0.index(max(dist_from_0))
    
    # Perform BFS from one endpoint of the diameter to find the third node
    _, _, dist_from_a = bfs(a, graph)
    
    # The third node should be the farthest node from 'a' that is not on the path between 'a' and 'b'
    max_dist = 0
    c = -1
    for i in range(n):
        if i != a and i != b and dist_from_a[i] > max_dist:
            max_dist = dist_from_a[i]
            c = i
    
    # Output the result
    print(diameter)
    print(a+1, b+1, c+1)

if __name__ == "__main__":
    main()