from heapq import heappop, heappush
import sys

def minimum_flight_cost(n, m, k, flights):
    # Create adjacency list for flights going to and from Metropolis (0)
    flights_to_metropolis = []
    flights_from_metropolis = []
    
    for day, f, t, cost in flights:
        if f == 0:  # Flight to Metropolis
            heappush(flights_to_metropolis, (day, cost))
        elif t == 0:  # Flight from Metropolis
            heappush(flights_from_metropolis, (day, cost))
    
    # Minimum cost to get all jury members to Metropolis
    total_cost = 0
    total_days = 0
    temp_days = []
    
    # Try to gather all jury members in Metropolis for k days
    while flights_to_metropolis and total_days < k:
        day, cost = heappop(flights_to_metropolis)
        heappush(temp_days, day)
        total_cost += cost
        total_days += 1
    
    # Check if we managed to gather them in k days
    if total_days < k:
        return -1
    
    # Minimum cost to send them back home
    while flights_from_metropolis:
        day, cost = heappop(flights_from_metropolis)
        # Remove days that are already used for getting to Metropolis
        while temp_days and temp_days[0] <= day:
            heappop(temp_days)
        if not temp_days:
            return -1
        heappop(temp_days)
        total_cost += cost
        total_days += 1
    
    return total_cost

# Reading input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])
flights = []

index = 3
for _ in range(m):
    d_i = int(data[index])
    f_i = int(data[index+1])
    t_i = int(data[index+2])
    c_i = int(data[index+3])
    flights.append((d_i, f_i, t_i, c_i))
    index += 4

# Calculate the minimum cost
result = minimum_flight_cost(n, m, k, flights)

# Print the result
print(result)