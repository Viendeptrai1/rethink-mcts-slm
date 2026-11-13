def min_day_to_start_playing(n, m, k, offers):
    from collections import defaultdict
    import bisect

    # Sort offers by day
    offers.sort()

    # Create a list of sale days for each type of microtransaction
    sale_days = defaultdict(list)
    for d, t in offers:
        sale_days[t].append(d)

    # Calculate the total number of microtransactions to order
    total_to_order = sum(k)

    # Calculate the minimum number of days Ivan needs to buy all microtransactions
    min_days = 0
    for i in range(1, n + 1):
        if k[i - 1] > 0:
            # Calculate the number of sale days for this type of microtransaction
            sale_days_count = len(sale_days[i])
            # Calculate the number of regular days for this type of microtransaction
            regular_days_count = k[i - 1] - sale_days_count
            # Add the number of days to the total
            min_days += regular_days_count * 2 + sale_days_count

    return min_days

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = list(map(int, data[2:n + 2]))
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