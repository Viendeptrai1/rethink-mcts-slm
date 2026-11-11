import sys
import heapq

def dijkstra(graph, start, n):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > dist[u]:
            continue
        
        for v, weight in graph[u]:
            distance = current_dist + weight
            
            if distance < dist[v]:
                dist[v] = distance
                heapq.heappush(pq, (distance, v))
    
    return dist

def find_optimal_teleport_city(n, m, edges, attacked_cities):
    graph = [[] for _ in range(n + 1)]
    
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    total_distances = [0] * (n + 1)
    
    for city in attacked_cities:
        distances = dijkstra(graph, city, n)
        for other_city in attacked_cities:
            total_distances[other_city] += distances[other_city]
    
    min_time = float('inf')
    optimal_city = -1
    
    for city in attacked_cities:
        if total_distances[city] < min_time or (total_distances[city] == min_time and city < optimal_city):
            min_time = total_distances[city]
            optimal_city = city
    
    return optimal_city, min_time

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    edges = []
    for _ in range(n - 1):
        u = int(data[index])
        v = int(data[index + 1])
        edges.append((u, v))
        index += 2
    
    attacked_cities = list(map(int, data[index:index + m]))
    
    optimal_city, min_time = find_optimal_teleport_city(n, m, edges, attacked_cities)
    
    print(optimal_city)
    print(min_time)

if __name__ == "__main__":
    main()