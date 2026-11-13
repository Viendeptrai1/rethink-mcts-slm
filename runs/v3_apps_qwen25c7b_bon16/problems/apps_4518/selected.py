from typing import List

def can_connect_districts(n: int, gang_ids: List[int]) -> str:
    # Check if it's possible to connect all districts without any two directly connected districts being in the same gang
    gangs = set(gang_ids)
    if len(gangs) == 1:
        return "NO"
    
    # Create a graph with nodes representing districts and edges representing potential connections
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if gang_ids[i] != gang_ids[j]:
                graph[i].append(j)
                graph[j].append(i)
    
    # Perform BFS to check if the graph is connected
    visited = [False] * n
    stack = [0]
    visited[0] = True
    
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
    
    if all(visited):
        # Generate the minimum spanning tree using DFS
        def dfs(node: int, parent: int):
            for neighbor in graph[node]:
                if neighbor != parent:
                    print(f"{node + 1} {neighbor + 1}")
                    dfs(neighbor, node)
        
        dfs(0, -1)
        return "YES"
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
    gang_ids = list(map(int, data[index:index + n]))
    index += n
    results.append(can_connect_districts(n, gang_ids))

# Print results
for result in results:
    print(result)