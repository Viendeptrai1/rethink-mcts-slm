import sys
from collections import defaultdict, deque

def min_day_to_order_microtransactions(n, m, k, offers):
    # Initialize the day when each type of microtransaction becomes available at sale
    sale_days = [float('inf')] * (n + 1)
    
    # Process each offer to update the earliest sale day for each type of microtransaction
    for d, t in offers:
        sale_days[t] = min(sale_days[t], d)
    
    # Initialize the queue for BFS
    queue = deque()
    visited = set()
    
    # Start from day 0 with 0 burles
    queue.append((0, 0))
    visited.add((0, 0))
    
    while queue:
        current_day, burles = queue.popleft()
        
        # Check if Ivan can buy all microtransactions on this day
        if all(burles >= k[i] * (2 if current_day < sale_days[i] else 1) for i in range(1, n + 1)):
            return current_day
        
        # Try to buy each type of microtransaction
        for i in range(1, n + 1):
            if burles >= k[i] * (2 if current_day < sale_days[i] else 1):
                # Calculate the new day and burles after buying all k[i] of type i
                new_day = current_day + 1
                new_burles = burles - k[i] * (2 if current_day < sale_days[i] else 1)
                
                if (new_day, new_burles) not in visited:
                    visited.add((new_day, new_burles))
                    queue.append((new_day, new_burles))
    
    return -1  # This line should never be reached if the problem constraints are met

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = list(map(int, data[2:2+n]))
offers = [(int(data[2+n+2*i]), int(data[2+n+2*i+1])) for i in range(m)]

# Output the result
print(min_day_to_order_microtransactions(n, m, k, offers))