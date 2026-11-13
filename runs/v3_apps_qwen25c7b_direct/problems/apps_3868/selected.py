import sys
from heapq import heappop, heappush

def min_cost_to_gather_jury(n, m, k, flights):
    # Create adjacency list for the graph
    graph = [[] for _ in range(n + 1)]
    for d, f, t, c in flights:
        if f == 0:
            graph[t].append((d, c))
        elif t == 0:
            graph[f].append((d, c))

    # Priority queue to store the minimum cost to reach each city on each day
    pq = []
    for i in range(1, n + 1):
        if (k + 1) * i <= 10**6:
            heappush(pq, ((k + 1) * i, i, 0))

    # Dictionary to store the minimum cost to reach each city on each day
    min_cost = {(i, j): float('inf') for i in range(k + 2) for j in range(n + 1)}
    for i in range(1, n + 1):
        min_cost[(k + 1, i)] = 0

    # Dijkstra's algorithm to find the minimum cost to reach each city on each day
    while pq:
        d, city, cost = heappop(pq)
        if d > min_cost[(city, d // (k + 1))]:
            continue
        for next_d, next_city, next_cost in graph[city]:
            new_cost = cost + next_cost
            if d + next_d <= 10**6 and new_cost < min_cost[(next_city, (d + next_d) // (k + 1))]:
                min_cost[(next_city, (d + next_d) // (k + 1))] = new_cost
                heappush(pq, ((d + next_d, next_city, new_cost)))

    # Find the minimum cost to gather all jury members in Metropolis for k days and send them back
    ans = float('inf')
    for i in range(1, n + 1):
        if min_cost[(i, k + 1)] != float('inf'):
            ans = min(ans, min_cost[(i, k + 1)])

    return ans if ans != float('inf') else -1

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
k = int(data[2])
flights = [(int(data[3 + 4 * i]), int(data[4 + 4 * i]), int(data[5 + 4 * i]), int(data[6 + 4 * i])) for i in range(m)]

# Output result
print(min_cost_to_gather_jury(n, m, k, flights))