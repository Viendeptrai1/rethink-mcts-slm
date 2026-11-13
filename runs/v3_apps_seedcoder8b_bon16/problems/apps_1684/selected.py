def check_symmetry(n, m, segments):
    from collections import defaultdict

    graph = defaultdict(list)

    # Create adjacency list for the segments
    for a, b in segments:
        graph[a].append(b)
        graph[b].append(a)

    # Check if the graph is bipartite
    color = {}

    def bfs(start):
        queue = [start]
        color[start] = 0  # Start coloring with 0
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]  # Alternate color
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        return True

    # Check each component of the graph
    for node in range(1, n + 1):
        if node not in color:
            if not bfs(node):
                return "No"
    
    return "Yes"

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

# Call the function and print the result
print(check_symmetry(n, m, segments))