import heapq
from collections import defaultdict

def min_cost_to_gather_olympiad(n, m, k, flights):
    # Create adjacency list for the graph
    graph = defaultdict(list)
    for d, f, t, c in flights:
        if f == 0:
            graph[t].append((d, c))
        else:
            graph[f].append((d, c))
    
    # Function to perform Dijkstra's algorithm
    def dijkstra(start):
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
    
    # Find the minimum cost to reach each city from Metropolis
    dist_to_metropolis = dijkstra(0)
    
    # Find the minimum cost to return from each city to Metropolis
    dist_from_metropolis = dijkstra(0)
    
    # Check if it's possible to gather all jury members in Metropolis for k days
    max_days_needed = 0
    for i in range(1, n + 1):
        max_days_needed = max(max_days_needed, dist_to_metropolis[i] + dist_from_metropolis[i])
    
    if max_days_needed > k:
        return -1
    
    # Calculate the total minimum cost
    total_cost = 0
    for i in range(1, n + 1):
        total_cost += dist_to_metropolis[i] + dist_from_metropolis[i]
    
    return total_cost

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

flights = []
index = 3
for _ in range(m):
    d = int(data[index])
    f = int(data[index + 1])
    t = int(data[index + 2])
    c = int(data[index + 3])
    flights.append((d, f, t, c))
    index += 4

# Output the result
result = min_cost_to_gather_olympiad(n, m, k, flights)
print(result)