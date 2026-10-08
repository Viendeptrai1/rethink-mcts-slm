import sys
from collections import defaultdict, deque

def min_day_to_start_playing(n, m, k, offers):
    # Initialize the day counter
    day = 0
    # Initialize the total burles Ivan has
    burles = 0
    # Initialize the remaining microtransactions for each type
    remaining = k[:]
    # Create a dictionary to store the days when each type of microtransaction is on sale
    sale_days = defaultdict(list)
    for d, t in offers:
        sale_days[t].append(d)
    
    # Priority queue to store the next available sale day for each type of microtransaction
    sale_queue = [deque(sale_days[i+1]) for i in range(n)]
    
    while True:
        day += 1
        burles += 1
        
        # Check if any microtransaction type has a sale today
        for i in range(n):
            if sale_queue[i] and sale_queue[i][0] == day:
                sale_queue[i].popleft()
        
        # Try to buy microtransactions
        for i in range(n):
            if remaining[i] > 0:
                if sale_queue[i]:
                    # Buy at sale price
                    if burles >= 1:
                        burles -= 1
                        remaining[i] -= 1
                else:
                    # Buy at regular price
                    if burles >= 2:
                        burles -= 2
                        remaining[i] -= 1
        
        # Check if all microtransactions are bought
        if all(x == 0 for x in remaining):
            return day

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = list(map(int, data[2:2+n]))
offers = [(int(data[2+n+2*i]), int(data[2+n+2*i+1])) for i in range(m)]

# Calculate and print the result
print(min_day_to_start_playing(n, m, k, offers))