import sys
import heapq
from collections import defaultdict, deque

def minimum_cost_to_gather_jury(n, m, k, flights):
    # Create adjacency list for flights
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    
    for d, f, t, c in flights:
        if f == 0:
            outgoing[d].append((t, c))
        elif t == 0:
            incoming[d].append((f, c))
    
    # Sort flights by day
    outgoing = dict(sorted(outgoing.items()))
    incoming = dict(sorted(incoming.items()))
    
    # Dijkstra-like approach to find minimum cost to reach Metropolis
    min_cost_to_metro = [float('inf')] * (n + 1)
    min_cost_to_metro[0] = 0
    pq = [(0, 0)]  # (cost, city)
    
    while pq:
        current_cost, city = heapq.heappop(pq)
        
        if current_cost > min_cost_to_metro[city]:
            continue
        
        # Check outgoing flights
        for day, (dest, cost) in outgoing.items():
            if day >= current_cost and dest != city:
                new_cost = day + cost
                if new_cost < min_cost_to_metro[dest]:
                    min_cost_to_metro[dest] = new_cost
                    heapq.heappush(pq, (new_cost, dest))
        
        # Check incoming flights
        for day, (src, cost) in incoming.items():
            if day >= current_cost and src != city:
                new_cost = day + cost
                if new_cost < min_cost_to_metro[src]:
                    min_cost_to_metro[src] = new_cost
                    heapq.heappush(pq, (new_cost, src))
    
    # Check if all jury members can be gathered in Metropolis for k days
    if any(cost == float('inf') for cost in min_cost_to_metro[1:]):
        return -1
    
    # Calculate the minimum cost to send all jury members back home
    total_cost = 0
    for day in range(1, k + 1):
        # Find the minimum cost to reach Metropolis on day `day`
        min_cost_to_metro_day = min(min_cost_to_metro[1:])
        total_cost += min_cost_to_metro_day
        
        # Update the costs for the next day
        for city in range(1, n + 1):
            if min_cost_to_metro[city] <= day:
                # Check outgoing flights
                for next_day, (dest, cost) in outgoing.items():
                    if next_day > day and dest != city:
                        new_cost = next_day + cost
                        min_cost_to_metro[dest] = min(min_cost_to_metro[dest], new_cost)
                
                # Check incoming flights
                for next_day, (src, cost) in incoming.items():
                    if next_day > day and src != city:
                        new_cost = next_day + cost
                        min_cost_to_metro[src] = min(min_cost_to_metro[src], new_cost)
    
    return total_cost

def main():
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
    
    result = minimum_cost_to_gather_jury(n, m, k, flights)
    print(result)

if __name__ == "__main__":
    main()