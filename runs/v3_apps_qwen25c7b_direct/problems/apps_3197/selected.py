def max_participants(n, k, preferences):
    graph = {i: set() for i in range(1, n + 1)}
    for i, pref in enumerate(preferences, start=1):
        if pref != i:
            graph[i].add(pref)
    
    def dfs(node, visited):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                stack.extend(graph[current] - visited)
    
    groups = []
    visited = set()
    for i in range(1, n + 1):
        if i not in visited:
            group = set()
            dfs(i, group)
            groups.append(group)
    
    return min(len(group) for group in groups if len(group) <= k)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

print(max_participants(n, k, preferences))