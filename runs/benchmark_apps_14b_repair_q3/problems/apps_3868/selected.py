import sys
import heapq

def min_cost_to_gather_olympiad_jury(n, m, k, flights):
    # Create adjacency lists for flights to and from Metropolis
    flights_to_metropolis = [[] for _ in range(n + 1)]
    flights_from_metropolis = [[] for _ in range(n + 1)]
    
    for d, f, t, c in flights:
        if f == 0:
            flights_to_metropolis[t].append((d, c))
        else:
            flights_from_metropolis[f].append((d, c))
    
    # Function to find the minimum cost to gather all jury members in Metropolis for k days
    def gather_in_metropolis():
        # Priority queue to store (cost, day) tuples
        pq = []
        # dp[i] will store the minimum cost to have all jury members in Metropolis up to day i
        dp = [float('inf')] * (k + 1)
        dp[0] = 0
        
        # Push the initial state into the priority queue
        heapq.heappush(pq, (0, 0))
        
        while pq:
            current_cost, current_day = heapq.heappop(pq)
            
            if current_cost > dp[current_day]:
                continue
            
            # Check flights to Metropolis
            for next_day, cost in flights_to_metropolis[0]:
                if next_day > current_day:
                    new_cost = current_cost + cost
                    if new_cost < dp[next_day]:
                        dp[next_day] = new_cost
                        heapq.heappush(pq, (new_cost, next_day))
            
            # Check flights from Metropolis
            for next_day, cost in flights_from_metropolis[0]:
                if next_day > current_day:
                    new_cost = current_cost + cost
                    if new_cost < dp[next_day]:
                        dp[next_day] = new_cost
                        heapq.heappush(pq, (new_cost, next_day))
        
        return dp[k]
    
    # Function to find the minimum cost to send all jury members back to their home cities
    def send_back_home():
        # Priority queue to store (cost, day) tuples
        pq = []
        # dp[i] will store the minimum cost to have all jury members sent back to their home cities up to day i
        dp = [float('inf')] * (k + 1)
        dp[k] = 0
        
        # Push the initial state into the priority queue
        heapq.heappush(pq, (0, k))
        
        while pq:
            current_cost, current_day = heapq.heappop(pq)
            
            if current_cost > dp[current_day]:
                continue
            
            # Check flights from Metropolis
            for next_day, cost in flights_from_metropolis[0]:
                if next_day < current_day:
                    new_cost = current_cost + cost
                    if new_cost < dp[next_day]:
                        dp[next_day] = new_cost
                        heapq.heappush(pq, (new_cost, next_day))
            
            # Check flights to Metropolis
            for next_day, cost in flights_to_metropolis[0]:
                if next_day < current_day:
                    new_cost = current_cost + cost
                    if new_cost < dp[next_day]:
                        dp[next_day] = new_cost
                        heapq.heappush(pq, (new_cost, next_day))
        
        return dp[0]
    
    # Calculate the minimum cost to gather all jury members in Metropolis for k days
    gather_cost = gather_in_metropolis()
    
    if gather_cost == float('inf'):
        return -1
    
    # Calculate the minimum cost to send all jury members back to their home cities
    send_back_cost = send_back_home()
    
    if send_back_cost == float('inf'):
        return -1
    
    # Total minimum cost
    total_cost = gather_cost + send_back_cost
    
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
result = min_cost_to_gather_olympiad_jury(n, m, k, flights)
print(result)