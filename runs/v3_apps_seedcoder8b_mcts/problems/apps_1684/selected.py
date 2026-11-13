def is_rotationally_symmetrical(n, m, segments):
    from collections import defaultdict

    # Create a graph to represent the segments
    graph = defaultdict(list)
    for a, b in segments:
        graph[a].append(b)
        graph[b].append(a)

    # Function to perform DFS and collect the path
    def dfs(node, visited, path):
        visited[node] = True
        path.append(node)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, visited, path)
        path.append(node)

    # Find a cycle in the graph
    visited = [False] * (n + 1)
    path = []
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, visited, path)
            if len(path) > 2:
                break

    # Check if the path forms a cycle
    if len(path) < 4 or path[0] != path[-1]:
        return "No"

    # Check if the cycle length is a divisor of n
    cycle_length = len(path) // 2
    if n % cycle_length == 0:
        return "Yes"
    else:
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

# Get the result
result = is_rotationally_symmetrical(n, m, segments)

# Print the result
print(result)