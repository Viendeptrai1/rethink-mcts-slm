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

def find_longest_path(graph):
    # Find the farthest node from an arbitrary starting node (node 0)
    dist = bfs(0, graph)
    farthest_node = dist.index(max(dist))
    
    # Find the farthest node from the farthest node found above
    dist = bfs(farthest_node, graph)
    farthest_node_2 = dist.index(max(dist))
    
    return farthest_node_2, max(dist)

def find_three_longest_paths(graph):
    # Find the first longest path
    node1, length1 = find_longest_path(graph)
    
    # Find the second longest path starting from the endpoint of the first longest path
    node2, length2 = find_longest_path(graph)
    
    # Find the third longest path starting from the endpoint of the second longest path
    node3, length3 = find_longest_path(graph)
    
    return node1, node2, node3, length1, length2, length3

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
    
    node1, node2, node3, length1, length2, length3 = find_three_longest_paths(graph)
    
    res = length1 + length2 + length3 - 2 * min(length1, length2, length3)
    
    print(res)
    print(node1 + 1, node2 + 1, node3 + 1)

if __name__ == "__main__":
    main()