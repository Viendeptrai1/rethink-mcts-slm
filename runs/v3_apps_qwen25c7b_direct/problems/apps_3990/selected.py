import sys
from collections import deque

def min_time_to_reach_n(n, m, railways):
    # Create adjacency lists for railways and roads
    rail_adj = [[] for _ in range(n + 1)]
    road_adj = [[] for _ in range(n + 1)]
    
    for u, v in railways:
        rail_adj[u].append(v)
        rail_adj[v].append(u)
        road_adj[u].append(v)
        road_adj[v].append(u)
    
    # Function to perform BFS and find the shortest path
    def bfs(start, adj_list):
        visited = [False] * (n + 1)
        queue = deque([(start, 0)])
        visited[start] = True
        
        while queue:
            node, dist = queue.popleft()
            if node == n:
                return dist
            for neighbor in adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, dist + 1))
        
        return float('inf')
    
    # Find the shortest path for the train (railways)
    train_time = bfs(1, rail_adj)
    
    # Find the shortest path for the bus (roads)
    bus_time = bfs(1, road_adj)
    
    # Check if either vehicle can reach town n
    if train_time == float('inf') or bus_time == float('inf'):
        return -1
    
    # Return the maximum of the two times
    return max(train_time, bus_time)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

railways = []
index = 2
for _ in range(m):
    u = int(data[index])
    v = int(data[index + 1])
    railways.append((u, v))
    index += 2

# Output the result
print(min_time_to_reach_n(n, m, railways))