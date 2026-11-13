def max_participants(n, k, preferences):
    graph = {i: set() for i in range(1, n + 1)}
    for i, x in enumerate(preferences, start=1):
        if i != x:
            graph[i].add(x)
    
    def dfs(node, visited):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                stack.extend(graph[current])
        return len(visited)
    
    groups = []
    visited = set()
    for i in range(1, n + 1):
        if i not in visited:
            groups.append(dfs(i, visited))
    
    total_groups = sum(1 for g in groups if g <= k) + sum(g - k for g in groups if g > k)
    return min(total_groups, n)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

print(max_participants(n, k, preferences))