def min_day_to_start_playing(n, m, k, offers):
    from collections import defaultdict

    # Total number of microtransactions Ivan needs to order
    total_needed = sum(k)
    
    # Mapping days to types of microtransactions that are on sale
    sale_days = defaultdict(set)
    for d, t in offers:
        sale_days[d].add(t)
    
    # We need to find the minimum day such that the sum of the needed items
    # which are not on sale costs more than the burles earned until that day.
    current_day = 0
    current_burles = 0
    ordered_burles = 0
    
    while ordered_burles < total_needed:
        current_day += 1
        current_burles += 1
        
        # Check for each type if it is in the sale_days on the current_day
        for t in range(1, n + 1):
            if t in sale_days[current_day] and k[t - 1] > 0:
                # If it is on sale and we need it, buy it at 1 burle
                ordered_burles += 1
                k[t - 1] -= 1
            elif k[t - 1] > 0:
                # If it is not on sale and we need it, buy it at 2 burles
                ordered_burles += 2
                k[t - 1] -= 1
    
    return current_day

if __name__ == "__main__":
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
    
    result = min_day_to_start_playing(n, m, k, offers)
    print(result)