import sys
from collections import defaultdict, deque

def min_day_to_order_microtransactions(n, m, k, offers):
    # Initialize the day when each type of microtransaction can be bought at full price
    full_price_days = [float('inf')] * (n + 1)
    
    # Initialize the day when each type of microtransaction can be bought at sale price
    sale_price_days = [float('inf')] * (n + 1)
    
    # Process the offers to determine the earliest sale days
    for d, t in offers:
        sale_price_days[t] = min(sale_price_days[t], d)
    
    # Calculate the minimum day to buy all microtransactions
    current_day = 0
    total_burles_needed = sum(k)
    
    while total_burles_needed > 0:
        current_day += 1
        
        # Check if any microtransaction type goes on sale today
        for t in range(1, n + 1):
            if sale_price_days[t] == current_day:
                full_price_days[t] = current_day
        
        # Try to buy microtransactions
        for t in range(1, n + 1):
            if k[t - 1] > 0:
                if current_day >= full_price_days[t]:
                    # Buy at full price
                    if k[t - 1] <= current_day // 2:
                        total_burles_needed -= k[t - 1]
                        k[t - 1] = 0
                    else:
                        total_burles_needed -= current_day // 2
                        k[t - 1] -= current_day // 2
                elif current_day >= sale_price_days[t]:
                    # Buy at sale price
                    if k[t - 1] <= current_day:
                        total_burles_needed -= k[t - 1]
                        k[t - 1] = 0
                    else:
                        total_burles_needed -= current_day
                        k[t - 1] -= current_day
    
    return current_day

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

k = list(map(int, data[2:2 + n]))

offers = []
index = 2 + n
for _ in range(m):
    d = int(data[index])
    t = int(data[index + 1])
    offers.append((d, t))
    index += 2

# Calculate and print the result
result = min_day_to_order_microtransactions(n, m, k, offers)
print(result)