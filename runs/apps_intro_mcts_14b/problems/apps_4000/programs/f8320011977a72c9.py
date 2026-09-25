import sys
from collections import defaultdict, deque

def bfs(start, graph):
    queue = deque([start])
    dist = [-1] * (len(graph) + 1)
    dist[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

def find_longest_path(start, graph):
    dist = bfs(start, graph)
    max_dist = max(dist)
    farthest_node = dist.index(max_dist)
    return farthest_node, max_dist

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[i]), int(data[i+1])) for i in range(1, 2*n, 2)]
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Find the first longest path
    start_node = 1
    _, _ = find_longest_path(start_node, graph)
    first_end, first_dist = find_longest_path(start_node, graph)
    
    # Find the second longest path
    _, _ = find_longest_path(first_end, graph)
    second_end, second_dist = find_longest_path(first_end, graph)
    
    # Find the third longest path
    _, _ = find_longest_path(second_end, graph)
    third_end, third_dist = find_longest_path(second_end, graph)
    
    # The result is the sum of the distances of the three longest paths
    res = first_dist + second_dist + third_dist
    
    # Print the result and the vertices
    print(res)
    print(first_end, second_end, third_end)

if __name__ == "__main__":
    main()