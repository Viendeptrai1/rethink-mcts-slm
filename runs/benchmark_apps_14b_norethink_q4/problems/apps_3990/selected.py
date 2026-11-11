import sys
import heapq

def min_time_to_reach_town_n(n, m, railways):
    # Create adjacency lists for railways and roads
    railway_adj = [[] for _ in range(n + 1)]
    road_adj = [[] for _ in range(n + 1)]
    
    for u, v in railways:
        railway_adj[u].append(v)
        railway_adj[v].append(u)
    
    # Roads exist between all pairs of towns that are not connected by a railway
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if j not in railway_adj[i]:
                road_adj[i].append(j)
                road_adj[j].append(i)
    
    # Priority queue for Dijkstra's algorithm
    pq = []
    # (time, town, vehicle_type) where vehicle_type is 0 for train and 1 for bus
    heapq.heappush(pq, (0, 1, 0))
    heapq.heappush(pq, (0, 1, 1))
    
    # Distance table for train and bus
    dist_train = [float('inf')] * (n + 1)
    dist_bus = [float('inf')] * (n + 1)
    dist_train[1] = 0
    dist_bus[1] = 0
    
    while pq:
        time, town, vehicle_type = heapq.heappop(pq)
        
        if vehicle_type == 0:  # Train
            for neighbor in railway_adj[town]:
                new_time = time + 1
                if new_time < dist_train[neighbor]:
                    dist_train[neighbor] = new_time
                    heapq.heappush(pq, (new_time, neighbor, 0))
        else:  # Bus
            for neighbor in road_adj[town]:
                new_time = time + 1
                if new_time < dist_bus[neighbor]:
                    dist_bus[neighbor] = new_time
                    heapq.heappush(pq, (new_time, neighbor, 1))
    
    # Find the maximum of the minimum times to reach town n for both vehicles
    max_min_time = max(dist_train[n], dist_bus[n])
    
    if max_min_time == float('inf'):
        return -1
    else:
        return max_min_time

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
print(min_time_to_reach_town_n(n, m, railways))