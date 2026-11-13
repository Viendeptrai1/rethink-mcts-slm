from sys import stdin
import heapq

def min_time_to_scare_all_cities(n, m, edges, attacked_cities):
    # Create adjacency list for the graph
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Calculate shortest paths from each attacked city to all other cities
    def dijkstra(start):
        dist = [float('inf')] * (n + 1)
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v in graph[u]:
                new_d = d + 1
                if new_d < dist[v]:
                    dist[v] = new_d
                    heapq.heappush(pq, (new_d, v))
        return dist

    min_time = float('inf')
    best_city = None
    for city in attacked_cities:
        dist = dijkstra(city)
        max_dist = max(dist[city] for city in attacked_cities)
        if max_dist < min_time or (max_dist == min_time and city < best_city):
            min_time = max_dist
            best_city = city

    return best_city, min_time

# Read input
n, m = map(int, stdin.readline().split())
edges = [tuple(map(int, stdin.readline().split())) for _ in range(n - 1)]
attacked_cities = list(map(int, stdin.readline().split()))

# Solve the problem
result_city, result_time = min_time_to_scare_all_cities(n, m, edges, attacked_cities)

# Output the result
print(result_city)
print(result_time)