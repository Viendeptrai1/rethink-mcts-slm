import sys
from collections import deque

def min_time_to_reach_n(n, m, railways):
    # Create adjacency lists for railways and roads
    railway_graph = [[] for _ in range(n + 1)]
    road_graph = [[] for _ in range(n + 1)]
    
    for u, v in railways:
        railway_graph[u].append(v)
        railway_graph[v].append(u)
    
    # Fill road graph with all possible roads except those that are railways
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if v not in railway_graph[u]:
                road_graph[u].append(v)
                road_graph[v].append(u)
    
    # BFS to find shortest path from 1 to n for train and bus
    def bfs(graph):
        queue = deque([(1, 0)])  # (current town, current time)
        visited = [False] * (n + 1)
        visited[1] = True
        distance = [float('inf')] * (n + 1)
        distance[1] = 0
        
        while queue:
            current, time = queue.popleft()
            for neighbor in graph[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    distance[neighbor] = time + 1
                    queue.append((neighbor, time + 1))
        
        return distance[n]
    
    train_time = bfs(railway_graph)
    bus_time = bfs(road_graph)
    
    if train_time == float('inf') or bus_time == float('inf'):
        return -1
    
    return max(train_time, bus_time)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
railways = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]

# Output the result
print(min_time_to_reach_n(n, m, railways))