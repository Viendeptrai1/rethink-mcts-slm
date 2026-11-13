import heapq

def min_coupons(N, trips):
    tickets = []
    coupons = 0
    current_zone = 0
    current_time = 0
    
    for zone, time in trips:
        while tickets and tickets[0][0] <= time:
            _, z1, z2 = heapq.heappop(tickets)
        
        if not tickets or zone < tickets[0][1] or zone > tickets[0][2]:
            coupons += 2 + abs(current_zone - zone)
            heapq.heappush(tickets, (time + 10000, min(current_zone, zone), max(current_zone, zone)))
        
        current_zone = zone
        current_time = time
    
    return coupons

# Read input
N = int(input())
trips = [tuple(map(int, input().split())) for _ in range(N)]

# Calculate and print result
result = min_coupons(N, trips)
print(result)