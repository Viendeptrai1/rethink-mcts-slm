import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    k = read_ints()
    offers = [read_ints() for _ in range(m)]
    
    # Sort offers by day
    offers.sort()
    
    # Priority queue to store the days when each type of microtransaction will be on sale
    sale_days = [[] for _ in range(n + 1)]
    for d, t in offers:
        heapq.heappush(sale_days[t], d)
    
    current_day = 0
    total_cost = 0
    
    for i in range(1, n + 1):
        count = k[i - 1]
        while count > 0:
            if sale_days[i] and sale_days[i][0] <= current_day:
                # Buy at sale price
                heapq.heappop(sale_days[i])
                total_cost += 1
            else:
                # Buy at regular price
                total_cost += 2
            current_day += 1
            count -= 1
    
    print(current_day)

if __name__ == "__main__":
    main()