def is_rotationally_symmetrical(n, m, segments):
    from collections import defaultdict

    # Create an adjacency list for the graph
    adjacency_list = defaultdict(list)
    for a, b in segments:
        adjacency_list[a].append(b)
        adjacency_list[b].append(a)

    # Function to perform DFS and collect the path
    def dfs(node, visited, path):
        visited[node] = True
        path.append(node)
        for neighbor in adjacency_list[node]:
            if not visited[neighbor]:
                dfs(neighbor, visited, path)

    # Find a cycle using DFS
    visited = [False] * (n + 1)
    path = []
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, visited, path)
            if len(path) > 0:
                break

    # Check if the path forms a cycle
    if len(path) < n:
        return "No"

    # Check if the path is a valid cycle
    for i in range(n):
        if path[i] not in adjacency_list[path[(i + 1) % n]]:
            return "No"

    # Check for rotational symmetry
    for k in range(1, n):
        if all((path[i] + k) % n == path[(i + 1) % n] for i in range(n)):
            return "Yes"

    return "No"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
segments = []

index = 2
for _ in range(m):
    a = int(data[index])
    b = int(data[index + 1])
    segments.append((a, b))
    index += 2

# Output the result
print(is_rotationally_symmetrical(n, m, segments))