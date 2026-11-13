from typing import List, Tuple
import heapq

def dijkstra(n: int, edges: List[Tuple[int, int]], start: int) -> List[int]:
    distances = [float('inf')] * (n + 1)
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in edges[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances

def min_time_to_scare_all_attacked_cities(n: int, m: int, edges: List[Tuple[int, int]], attacked_cities: List[int]) -> Tuple[int, int]:
    graph = [[] for _ in range(n + 1)]
    
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    max_distances = []
    
    for city in range(1, n + 1):
        distances = dijkstra(n, graph, city)
        max_distance = max(distances[city] for city in attacked_cities)
        max_distances.append((max_distance, city))
    
    min_max_distance, best_city = min(max_distances)
    
    return best_city, min_max_distance

# Input reading
n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]
attacked_cities = list(map(int, input().split()))

# Output result
best_city, min_time = min_time_to_scare_all_attacked_cities(n, m, edges, attacked_cities)
print(best_city)
print(min_time)