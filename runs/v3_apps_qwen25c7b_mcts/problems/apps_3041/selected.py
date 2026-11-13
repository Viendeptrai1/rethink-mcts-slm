import sys
from typing import List

def min_coupons(N: int, trips: List[List[int]]) -> int:
    trips.sort(key=lambda x: (x[1], x[0]))
    tickets = []
    current_zone = 0
    total_coupons = 0
    
    for zone, time in trips:
        while tickets and tickets[-1][1] < time:
            tickets.pop()
        
        if not tickets or tickets[-1][0] > zone:
            cost = 2 + abs(zone - current_zone)
            total_coupons += cost
            tickets.append((zone, time + 10000))
            current_zone = zone
    
    return total_coupons

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    trips = [[int(data[i*2+1]), int(data[i*2+2])] for i in range(N)]
    
    result = min_coupons(N, trips)
    print(result)