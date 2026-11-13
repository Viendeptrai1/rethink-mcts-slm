import sys

def min_coupons(N, trips):
    trips.sort(key=lambda x: x[1])
    tickets = []
    current_time = 0
    total_coupons = 0
    
    for zone, time in trips:
        while tickets and tickets[0][1] < time:
            _, end_time, cost = heapq.heappop(tickets)
            current_time = end_time
        
        if not tickets or zone > tickets[-1][0]:
            cost = 2 + abs(zone - tickets[-1][0]) if tickets else 0
            heapq.heappush(tickets, (zone, time + 10000, cost))
            total_coupons += cost
    
    return total_coupons

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    trips = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(N)]
    
    result = min_coupons(N, trips)
    print(result)