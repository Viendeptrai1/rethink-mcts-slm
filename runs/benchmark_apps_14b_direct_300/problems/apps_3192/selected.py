import sys
from collections import defaultdict, deque

def find_shortest_cycle(n, files, dependencies):
    # Build the graph
    graph = defaultdict(list)
    for i in range(n):
        file_name = files[i]
        k = dependencies[i][1]
        for j in range(k):
            imported_file = dependencies[i][2 + j].strip()
            graph[file_name].append(imported_file)
    
    # Function to perform BFS and detect cycles
    def bfs(start):
        queue = deque([(start, [start])])
        visited = set()
        while queue:
            node, path = queue.popleft()
            if node in visited:
                return path[path.index(node):]
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return None
    
    # Check for cycles
    for file_name in files:
        cycle = bfs(file_name)
        if cycle:
            return cycle
    
    return "SHIP IT"

# Read input
input = sys.stdin.read
data = input().splitlines()

n = int(data[0])
files = data[1].split()
dependencies = []
index = 2
for i in range(n):
    dependencies.append(data[index].split())
    index += int(data[index][1]) + 1

# Find and print the shortest cycle
result = find_shortest_cycle(n, files, dependencies)
print(" ".join(result))