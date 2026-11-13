import sys
import heapq
from collections import defaultdict

def minimum_cost_to_gather_jury(n, m, k, flights):
    # Create adjacency list for flights
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    
    for d, f, t, c in flights:
        if f == 0:
            outgoing[0].append((d, t, c))
        elif t == 0:
            incoming[0].append((d, f, c))
        else:
            outgoing[f].append((d, t, c))
            incoming[t].append((d, f, c))
    
    # Function to find minimum cost to reach city 0 from any city
    def find_min_cost_to_zero(adj_list):
        min_cost = [float('inf')] * (n + 1)
        min_cost[0] = 0
        pq = [(0, 0)]  # (cost, city)
        
        while pq:
            cost, city = heapq.heappop(pq)
            if cost > min_cost[city]:
                continue
            for day, next_city, flight_cost in adj_list[city]:
                new_cost = cost + flight_cost
                if new_cost < min_cost[next_city]:
                    min_cost[next_city] = new_cost
                    heapq.heappush(pq, (new_cost, next_city))
        
        return min_cost
    
    # Find minimum cost to reach city 0 from each city
    min_cost_to_zero = find_min_cost_to_zero(outgoing)
    min_cost_from_zero = find_min_cost_to_zero(incoming)
    
    # Calculate total minimum cost
    total_cost = 0
    for city in range(1, n + 1):
        if min_cost_to_zero[city] == float('inf') or min_cost_from_zero[city] == float('inf'):
            return -1
        total_cost += min_cost_to_zero[city] + min_cost_from_zero[city]
    
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