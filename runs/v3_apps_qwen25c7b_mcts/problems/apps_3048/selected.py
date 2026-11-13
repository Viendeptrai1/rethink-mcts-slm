from collections import defaultdict
import sys

def dfs(graph, node, parent, path_length):
    if path_length == 2:
        return 1
    count = 0
    for neighbor in graph[node]:
        if neighbor != parent:
            count += dfs(graph, neighbor, node, path_length + 1)
    return count

def count_optimal_paths(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    total_count = 0
    for i in range(1, n + 1):
        total_count += dfs(graph, i, None, 0)
    
    return total_count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = []
    index = 1
    for _ in range(n - 1):
        u = int(data[index])
        v = int(data[index + 1])
        edges.append((u, v))
        index += 2
    
    result = count_optimal_paths(n, edges)
    print(result)