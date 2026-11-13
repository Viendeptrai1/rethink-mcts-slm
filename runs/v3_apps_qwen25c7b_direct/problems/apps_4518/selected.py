from collections import defaultdict, deque

def find_gang_roads(n, gangs):
    # Create a graph where nodes are districts and edges are potential roads
    graph = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            if gangs[i] != gangs[j]:
                graph[i].append(j)
                graph[j].append(i)
    
    # Check if there are enough edges to form a spanning tree
    if len(graph) < n - 1:
        return "NO"
    
    # Use BFS to check if the graph is connected
    visited = set()
    queue = deque([0])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    
    if len(visited) == n:
        # Extract a spanning tree
        edges = []
        parent = [-1] * n
        stack = [0]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor != parent[node]:
                    edges.append((node, neighbor))
                    parent[neighbor] = node
                    stack.append(neighbor)
        return "YES\n" + "\n".join(f"{u+1} {v+1}" for u, v in edges)
    else:
        return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Process each test case
index = 0
results = []
for _ in range(int(data[index])):
    index += 1
    n = int(data[index])
    index += 1
    gangs = list(map(int, data[index:index+n]))
    index += n
    result = find_gang_roads(n, gangs)
    results.append(result)

# Print results
for result in results:
    print(result)