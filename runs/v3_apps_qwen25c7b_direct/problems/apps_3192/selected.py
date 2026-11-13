from collections import defaultdict, deque

def find_shortest_cycle(n, files, dependencies):
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for i in range(n):
        file_name, k = dependencies[i][0], int(dependencies[i][1])
        for j in range(k):
            dep_file = dependencies[i][j + 2]
            graph[file_name].append(dep_file)
            in_degree[files.index(dep_file)] += 1
    
    queue = deque([file for file in files if in_degree[files.index(file)] == 0])
    visited = set()
    parent = {file: None for file in files}
    
    while queue:
        current = queue.popleft()
        visited.add(current)
        
        for neighbor in graph[current]:
            in_degree[files.index(neighbor)] -= 1
            if in_degree[files.index(neighbor)] == 0:
                queue.append(neighbor)
                parent[neighbor] = current
    
    stack = []
    for node in files:
        if node not in visited:
            current = node
            while current is not None:
                stack.append(current)
                current = parent[current]
    
    if len(stack) > 1:
        return ' '.join(stack[::-1])
    else:
        return "SHIP IT"

# Read input
n = int(input())
files = input().split()
dependencies = [input().split() for _ in range(n)]

# Find and print the result
result = find_shortest_cycle(n, files, dependencies)
print(result)