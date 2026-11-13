import heapq
from collections import defaultdict

def min_cost_to_gather_jury(n, m, k, flights):
    # Build adjacency list for flights
    graph = defaultdict(list)
    for d, f, t, c in flights:
        if f == 0:
            graph[t].append((d, c))
        elif t == 0:
            graph[f].append((d, c))

    # Priority queue to store the cheapest flights for each day
    pq = []
    for d, f, t, c in flights:
        if f != 0 and t != 0:
            heapq.heappush(pq, (c, d, f, t))

    # Dictionary to store the earliest day a jury member can return to their city
    return_day = [float('inf')] * (n + 1)
    return_day[0] = 0

    # Process the flights to find the minimum cost to gather all jury members in Metropolis
    while pq:
        c, d, f, t = heapq.heappop(pq)
        if d > k:
            continue
        if return_day[f] < d:
            continue
        if return_day[t] < d:
            continue
        return_day[t] = max(return_day[t], d + 1)
        if return_day[t] <= k:
            return_day[f] = max(return_day[f], d + 1)

    # Check if all jury members can be gathered in Metropolis within k days
    if any(day > k for day in return_day[1:]):
        return -1

    # Calculate the total cost of the flights
    total_cost = sum(c for c, d, f, t in flights if d <= k and (f == 0 or t == 0))
    return total_cost

# Example usage
if __name__ == "__main__":
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
    
    result = min_cost_to_gather_jury(n, m, k, flights)
    print(result)