import sys
from collections import defaultdict

sys.setrecursionlimit(10**6)

def count_valid_paintings(N, edges, M, restrictions):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    def dfs(node, parent):
        children = []
        for child in graph[node]:
            if child != parent:
                children.append(dfs(child, node))
        return (children, node)

    tree = dfs(1, 0)

    def count_ways(node, parent, restrictions_met):
        children = [c for c in node[0] if c[1] != parent]
        total_ways = 1
        black_ways = 1

        for child in children:
            total_ways *= 2
            child_ways = count_ways(child, node[1], restrictions_met)
            black_ways *= child_ways[1]
            restrictions_met |= child_ways[2]

        if any(r[0] == node[1] and r[1] == parent for r in restrictions) and not restrictions_met:
            return (total_ways, 0, restrictions_met)
        
        return (total_ways, black_ways, restrictions_met | any(r[0] == node[1] or r[1] == node[1] for r in restrictions))

    result = count_ways(tree, 0, False)
    return result[0] - result[1]

N = int(input())
edges = [tuple(map(int, input().split())) for _ in range(N-1)]
M = int(input())
restrictions = [tuple(map(int, input().split())) for _ in range(M)]

print(count_valid_paintings(N, edges, M, restrictions))