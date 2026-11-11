import sys
from collections import defaultdict

def min_cost_to_gather_jury(n, m, k, flights):
    # Separate flights into incoming and outgoing based on Metropolis (city 0)
    incoming_flights = defaultdict(list)
    outgoing_flights = defaultdict(list)
    
    for d, f, t, c in flights:
        if f == 0:
            incoming_flights[t].append((d, c))
        else:
            outgoing_flights[f].append((d, c))
    
    # Sort flights by day
    for city in incoming_flights:
        incoming_flights[city].sort()
    for city in outgoing_flights:
        outgoing_flights[city].sort()
    
    # Priority queues to track the earliest available return flights
    import heapq
    return_flights = [heapq.heapify([]) for _ in range(n + 1)]
    
    total_cost = 0
    
    # Track the last day each jury member returns to Metropolis
    last_return_days = [-1] * (n + 1)
    
    for day in range(1, 10**6 + 1):
        # Process incoming flights for the current day
        for city in incoming_flights:
            while incoming_flights[city] and incoming_flights[city][0][0] == day:
                _, cost = incoming_flights[city].pop(0)
                heapq.heappush(return_flights[city], day + k)
                total_cost += cost
        
        # Process outgoing flights for the current day
        for city in outgoing_flights:
            while outgoing_flights[city] and outgoing_flights[city][0][0] == day:
                _, cost = outgoing_flights[city].pop(0)
                if not return_flights[city]:
                    return -1  # No available return flight
                return_day = heapq.heappop(return_flights[city])
                if return_day < day:
                    return -1  # Conflict with another flight
                total_cost += cost
    
    # Check if all jury members have returned to their home cities
    for city in range(1, n + 1):
        if return_flights[city]:
            return -1
    
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