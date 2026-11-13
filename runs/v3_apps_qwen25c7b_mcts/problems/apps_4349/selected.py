import sys
from collections import defaultdict

def min_day_to_start_playing(n, m, k, offers):
    # Initialize the cost dictionary with the usual price
    cost = {i+1: 2 for i in range(n)}
    
    # Update the cost dictionary with the sale price for each offer
    for d, t in offers:
        cost[t] = 1
    
    # Sort the offers by day
    offers.sort()
    
    # Dictionary to store the earliest day each type of microtransaction becomes available on sale
    sale_days = defaultdict(lambda: float('inf'))
    for d, t in offers:
        sale_days[t] = min(sale_days[t], d)
    
    # Calculate the total cost of buying all microtransactions
    total_cost = sum(k[i] * cost[i+1] for i in range(n))
    
    # Initialize variables to track the current day and the number of burles earned
    current_day = 0
    burles_earned = 0
    
    # Iterate until Ivan has enough burles to buy all microtransactions
    while burles_earned < total_cost:
        current_day += 1
        burles_earned += 1
        
        # Check if there are any microtransactions of any type that become available on sale today
        for i in range(n):
            if sale_days[i+1] == current_day:
                burles_earned -= cost[i+1]
                cost[i+1] = 1
                burles_earned += 1
    
    return current_day

# Read input from stdin
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

k = list(map(int, data[2:2+n]))
offers = []

for i in range(m):
    d = int(data[2+n + 2*i])
    t = int(data[2+n + 2*i + 1])
    offers.append((d, t))

# Call the function and print the result
print(min_day_to_start_playing(n, m, k, offers))