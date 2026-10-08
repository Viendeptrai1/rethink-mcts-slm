import sys
from collections import deque

def max_participants(n, k, preferences):
    # Create a graph where each node points to the node it depends on
    graph = [[] for _ in range(n + 1)]
    indegree = [0] * (n + 1)
    
    for i in range(1, n + 1):
        if preferences[i - 1] != i:
            graph[preferences[i - 1]].append(i)
            indegree[i] += 1
    
    # Initialize the queue with nodes that have zero indegree
    queue = deque()
    for i in range(1, n + 1):
        if indegree[i] == 0:
            queue.append(i)
    
    # Perform BFS to find the maximum number of participants
    selected = 0
    while queue:
        current = queue.popleft()
        selected += 1
        if selected > k:
            break
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return selected

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

# Output the result
print(max_participants(n, k, preferences))