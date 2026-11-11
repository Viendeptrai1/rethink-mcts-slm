import sys
import heapq

def min_cost_to_gather_jury(n, m, k, flights):
    # Create adjacency lists for flights
    flights_to_metropolis = [[] for _ in range(n + 1)]
    flights_from_metropolis = [[] for _ in range(n + 1)]
    
    for d, f, t, c in flights:
        if f == 0:
            flights_to_metropolis[t].append((d, c))
        else:
            flights_from_metropolis[f].append((d, c))
    
    # Function to find the minimum cost to reach metropolis on or before day `end_day`
    def dijkstra_to_metropolis(end_day):
        dist = [float('inf')] * (n + 1)
        dist[0] = 0
        pq = [(0, 0)]  # (cost, city)
        
        while pq:
            cost, city = heapq.heappop(pq)
            if cost > dist[city]:
                continue
            for d, c in flights_to_metropolis[city]:
                if d <= end_day:
                    new_cost = cost + c
                    if new_cost < dist[d]:
                        dist[d] = new_cost
                        heapq.heappush(pq, (new_cost, d))
        
        return dist
    
    # Function to find the minimum cost to leave metropolis on or after day `start_day`
    def dijkstra_from_metropolis(start_day):
        dist = [float('inf')] * (n + 1)
        dist[0] = 0
        pq = [(0, 0)]  # (cost, city)
        
        while pq:
            cost, city = heapq.heappop(pq)
            if cost > dist[city]:
                continue
            for d, c in flights_from_metropolis[city]:
                if d >= start_day:
                    new_cost = cost + c
                    if new_cost < dist[d]:
                        dist[d] = new_cost
                        heapq.heappush(pq, (new_cost, d))
        
        return dist
    
    # Find the minimum cost to reach metropolis on or before day `k`
    dist_to_metropolis = dijkstra_to_metropolis(k)
    
    # Find the minimum cost to leave metropolis on or after day `k + 1`
    dist_from_metropolis = dijkstra_from_metropolis(k + 1)
    
    # Calculate the total minimum cost
    total_cost = 0
    for i in range(1, n + 1):
        if dist_to_metropolis[i] == float('inf') or dist_from_metropolis[i] == float('inf'):
            return -1
        total_cost += dist_to_metropolis[i] + dist_from_metropolis[i]
    
    return total_cost

# Read input
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
result = min_cost_to_gather_jury(n, m, k, flights)
print(result)