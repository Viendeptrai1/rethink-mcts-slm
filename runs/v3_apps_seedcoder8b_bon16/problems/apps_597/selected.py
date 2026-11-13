import sys
from collections import deque

def solve():
    n, m = map(int, input().split())
    
    # Create adjacency list
    graph = [[] for _ in range(n+1)]
    for _ in range(n-1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    # Read attacked cities
    attacked = list(map(int, input().split()))
    
    # BFS to find distances from each node
    def bfs(start):
        distances = [-1] * (n+1)
        distances[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        return distances
    
    # Find distances from all nodes to each attacked city
    distances = [bfs(city) for city in attacked]
    
    # Find the city to teleport to
    teleport_city = 0
    min_time = float('inf')
    for city in range(1, n+1):
        max_distance = max(dist[city] for dist in distances)
        if max_distance < min_time:
            min_time = max_distance
            teleport_city = city
    
    print(teleport_city)
    print(min_time)

solve()