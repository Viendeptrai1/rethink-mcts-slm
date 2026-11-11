import sys
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > dist[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return dist

def min_time_to_reach_n(n, m, railways):
    # Build the graph for railways
    railway_graph = {i: {} for i in range(1, n+1)}
    for u, v in railways:
        railway_graph[u][v] = 1
        railway_graph[v][u] = 1
    
    # Build the graph for roads (complement of railway graph)
    road_graph = {i: {} for i in range(1, n+1)}
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if j not in railway_graph[i]:
                road_graph[i][j] = 1
                road_graph[j][i] = 1
    
    # Find shortest paths from 1 to n for both railway and road graphs
    railway_dist = dijkstra(railway_graph, 1)
    road_dist = dijkstra(road_graph, 1)
    
    if railway_dist[n] == float('inf') or road_dist[n] == float('inf'):
        return -1
    
    # Calculate the minimum time for both to reach n without meeting at any intermediate point
    min_time = float('inf')
    for i in range(2, n):
        if railway_dist[i] != float('inf') and road_dist[i] != float('inf'):
            min_time = min(min_time, max(railway_dist[i], road_dist[i]))
    
    return min(min_time, max(railway_dist[n], road_dist[n]))

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