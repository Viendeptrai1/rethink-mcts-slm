import sys
from heapq import heappop, heappush

def serve_customers():
    # Read input
    input = sys.stdin.read
    data = input().split()
    
    # Parse input
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    c = list(map(int, data[index:index + n]))
    index += n
    
    orders = []
    for _ in range(m):
        t = int(data[index])
        d = int(data[index + 1])
        index += 2
        orders.append((t - 1, d))
    
    # Initialize heap for cheap foods
    heap = []
    for i in range(n):
        if a[i] > 0:
            heappush(heap, (c[i], i))
    
    # Process each customer
    results = []
    for t, d in orders:
        current_cost = 0
        while d > 0 and heap:
            cost, i = heappop(heap)
            if a[i] == 0:
                continue
            count = min(d, a[i])
            current_cost += count * cost
            a[i] -= count
            d -= count
            if a[i] > 0:
                heappush(heap, (cost, i))
        
        results.append(current_cost if d == 0 else 0)
    
    # Output results
    for result in results:
        print(result)

serve_customers()