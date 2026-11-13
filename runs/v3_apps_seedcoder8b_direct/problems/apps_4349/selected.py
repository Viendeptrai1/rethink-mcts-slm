def min_day_to_start_playing(n, m, k, offers):
    from collections import defaultdict
    import heapq

    # Create a dictionary to store the sale days for each type of microtransaction
    sale_days = defaultdict(list)
    for d, t in offers:
        sale_days[t].append(d)

    # Sort the sale days for each type
    for t in sale_days:
        sale_days[t].sort()

    # Priority queue to keep track of the next sale day for each type
    sale_heap = []
    for t in range(1, n + 1):
        if sale_days[t]:
            heapq.heappush(sale_heap, (sale_days[t][0], t))

    # Calculate the minimum day to buy all microtransactions
    current_day = 0
    total_burles = 0
    required_burles = sum(k)

    while total_burles < required_burles:
        current_day += 1

        # Check if there's a sale on the current day
        if sale_heap and sale_heap[0][0] == current_day:
            sale_day, t = heapq.heappop(sale_heap)
            # Buy one microtransaction of type t for 1 burle
            total_burles += 1
            # If there are more sale days for this type, push the next one to the heap
            if len(sale_days[t]) > 1:
                heapq.heappush(sale_heap, (sale_days[t][1], t))
        else:
            # Buy one microtransaction of any type for 2 burles
            total_burles += 2

    return current_day

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = list(map(int, data[2:n+2]))
offers = []

index = n + 2
for _ in range(m):
    d = int(data[index])
    t = int(data[index + 1])
    offers.append((d, t))
    index += 2

# Calculate and print the result
result = min_day_to_start_playing(n, m, k, offers)
print(result)