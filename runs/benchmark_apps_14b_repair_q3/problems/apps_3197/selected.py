import sys

def max_participants(n, k, preferences):
    # Create a graph where each node points to its preferred companion
    graph = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        graph[preferences[i - 1]].append(i)
    
    # Array to keep track of visited nodes
    visited = [False] * (n + 1)
    # Array to keep track of the matching
    match = [-1] * (n + 1)
    
    def dfs(u):
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True
                if match[v] == -1 or dfs(match[v]):
                    match[v] = u
                    return True
        return False
    
    # Try to find a matching for each participant
    count = 0
    for i in range(1, n + 1):
        if not visited[i]:
            visited = [False] * (n + 1)
            if dfs(i):
                count += 1
    
    # The result is the minimum of the number of matched pairs and the bus capacity
    return min(count, k)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

# Output the result
print(max_participants(n, k, preferences))