from heapq import heappop, heappush

def min_cost_to_gather_jury(n, m, k, flights):
    graph = [[] for _ in range(n + 1)]
    
    for d, f, t, c in flights:
        if f == 0:
            graph[t].append((d, c))
        elif t == 0:
            graph[f].append((d, c))
    
    def dijkstra(start, end, k):
        pq = [(0, start, 0)]  # (current_cost, current_city, current_day)
        visited = set()
        
        while pq:
            cost, city, day = heappop(pq)
            
            if city == end and day <= k:
                return cost
            
            if (city, day) in visited:
                continue
            visited.add((city, day))
            
            for next_day, next_cost in graph[city]:
                if day + next_day > k:
                    continue
                heappush(pq, (cost + next_cost, city, day + next_day))
        
        return float('inf')
    
    total_cost = 0
    for i in range(1, n + 1):
        cost = dijkstra(i, 0, k)
        if cost == float('inf'):
            return -1
        total_cost += cost
    
    return total_cost

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

flights = []
for i in range(m):
    d = int(data[3 + i * 4]) - 1
    f = int(data[4 + i * 4])
    t = int(data[5 + i * 4])
    c = int(data[6 + i * 4])
    flights.append((d, f, t, c))

# Output result
print(min_cost_to_gather_jury(n, m, k, flights))