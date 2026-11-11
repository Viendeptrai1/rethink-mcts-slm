import sys
from collections import defaultdict

def dfs(node, parent, target, visited, graph):
    if node == target:
        return True
    visited[node] = True
    for neighbor in graph[node]:
        if neighbor != parent and not visited[neighbor]:
            if dfs(neighbor, node, target, visited, graph):
                return True
    return False

def count_valid_colorings(N, edges, M, restrictions):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    total_ways = 2 ** (N - 1)
    
    for u, v in restrictions:
        valid_ways = 0
        for mask in range(total_ways):
            visited = [False] * (N + 1)
            path_has_black = False
            for i, (a, b) in enumerate(edges):
                if (mask & (1 << i)) > 0:
                    if dfs(a, -1, b, visited, graph) or dfs(b, -1, a, visited, graph):
                        path_has_black = True
                        break
            if path_has_black:
                valid_ways += 1
        total_ways = valid_ways
    
    return total_ways

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    edges = []
    for _ in range(N - 1):
        a = int(data[index])
        b = int(data[index + 1])
        edges.append((a, b))
        index += 2
    
    M = int(data[index])
    index += 1
    restrictions = []
    for _ in range(M):
        u = int(data[index])
        v = int(data[index + 1])
        restrictions.append((u, v))
        index += 2
    
    result = count_valid_colorings(N, edges, M, restrictions)
    print(result)

if __name__ == "__main__":
    main()