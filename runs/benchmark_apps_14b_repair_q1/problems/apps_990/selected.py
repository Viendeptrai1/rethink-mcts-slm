import sys
from collections import defaultdict

def count_valid_paintings(N, edges, M, restrictions):
    def dfs(node, parent, color):
        if node in visited:
            return
        visited.add(node)
        colors[node] = color
        for neighbor in graph[node]:
            if neighbor != parent:
                dfs(neighbor, node, 1 - color)

    def is_valid_painting():
        for u, v in restrictions:
            lca = find_lca(u, v)
            if colors[u] == colors[v] == colors[lca]:
                return False
        return True

    def find_lca(u, v):
        depth = {}
        def assign_depth(node, parent, d):
            if node in depth:
                return
            depth[node] = d
            for neighbor in graph[node]:
                if neighbor != parent:
                    assign_depth(neighbor, node, d + 1)
        assign_depth(u, -1, 0)
        assign_depth(v, -1, 0)
        if depth[u] > depth[v]:
            u, v = v, u
        while depth[u] < depth[v]:
            v = parent[v]
        while u != v:
            u = parent[u]
            v = parent[v]
        return u

    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    total_ways = 0
    for i in range(1 << (N - 1)):
        colors = [0] * (N + 1)
        visited = set()
        parent = [-1] * (N + 1)
        for j in range(N - 1):
            if i & (1 << j):
                a, b = edges[j]
                if a not in visited:
                    dfs(a, -1, 0)
                if b not in visited:
                    dfs(b, -1, 1)
                parent[b] = a
            else:
                a, b = edges[j]
                if a not in visited:
                    dfs(a, -1, 1)
                if b not in visited:
                    dfs(b, -1, 0)
                parent[a] = b
        if is_valid_painting():
            total_ways += 1

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
    
    result = count_valid_paintings(N, edges, M, restrictions)
    print(result)

if __name__ == "__main__":
    main()