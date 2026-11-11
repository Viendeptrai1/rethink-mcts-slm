import sys
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def min_time_to_reach_n(n, m, railways):
    # Create adjacency lists for railways and roads
    railway_graph = {i: {} for i in range(1, n + 1)}
    road_graph = {i: {} for i in range(1, n + 1)}
    
    for u, v in railways:
        railway_graph[u][v] = 1
        railway_graph[v][u] = 1
    
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if j not in railway_graph[i]:
                road_graph[i][j] = 1
                road_graph[j][i] = 1
    
    # Find shortest paths for train and bus
    train_distances = dijkstra(railway_graph, 1)
    bus_distances = dijkstra(road_graph, 1)
    
    # Check if either cannot reach town n
    if train_distances[n] == float('inf') or bus_distances[n] == float('inf'):
        return -1
    
    # Find the minimum time such that train and bus do not meet at any intermediate town
    max_time = float('inf')
    for i in range(1, n):
        if train_distances[i] != float('inf') and bus_distances[i] != float('inf'):
            max_time = min(max_time, max(train_distances[i], bus_distances[i]))
    
    return max(train_distances[n], bus_distances[n], max_time)

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