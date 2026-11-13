import sys
from heapq import heappop, heappush

def dijkstra(graph, start, n):
    distances = [float('inf')] * (n + 1)
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heappop(pq)
        
        if current_dist > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(pq, (distance, neighbor))
    
    return distances

def min_time_to_reach_n(n, m, railways):
    graph_railways = [[] for _ in range(n + 1)]
    graph_roads = [[] for _ in range(n + 1)]
    
    for u, v in railways:
        graph_railways[u].append((v, 1))
        graph_railways[v].append((u, 1))
    
    # Add roads where there are no railways
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) not in railways and (j, i) not in railways:
                graph_roads[i].append((j, 1))
                graph_roads[j].append((i, 1))
    
    dist_train = dijkstra(graph_railways, 1, n)
    dist_bus = dijkstra(graph_roads, 1, n)
    
    if dist_train[n] == float('inf') or dist_bus[n] == float('inf'):
        return -1
    
    return max(dist_train[n], dist_bus[n])

input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
railways = [(int(data[2 + 2*i]), int(data[3 + 2*i])) for i in range(m)]

result = min_time_to_reach_n(n, m, railways)
print(result)