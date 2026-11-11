import sys
import heapq

def min_cost_to_gather_jury(n, m, k, flights):
    # Create adjacency list for flights
    adj = [[] for _ in range(n + 1)]
    for d, f, t, c in flights:
        if f == 0:
            adj[t].append((d, c))
        else:
            adj[f].append((d, c))
    
    # Function to find the minimum cost to reach Metropolis by day d
    def dijkstra(start, end, max_day):
        dist = [float('inf')] * (max_day + 1)
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for nd, c in adj[u]:
                if nd <= max_day and dist[nd] > d + c:
                    dist[nd] = d + c
                    heapq.heappush(pq, (dist[nd], nd))
        return dist[end]
    
    # Check if it's possible to gather all jury members in Metropolis for k days
    possible = True
    for i in range(1, n + 1):
        if dijkstra(i, 0, k) == float('inf'):
            possible = False
            break
    
    if not possible:
        return -1
    
    # Find the minimum cost to send all jury members back home after k days
    total_cost = 0
    for i in range(1, n + 1):
        min_cost = float('inf')
        for d, c in adj[i]:
            if d >= k:
                min_cost = min(min_cost, c)
        if min_cost == float('inf'):
            return -1
        total_cost += min_cost
    
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