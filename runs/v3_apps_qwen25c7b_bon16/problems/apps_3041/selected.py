def min_coupons(N, trips):
    tickets = []
    current_zone = 0
    total_coupons = 0
    
    for Z, T in trips:
        while current_zone < Z:
            start_time = max(T, current_zone * 1000)
            end_time = start_time + 10000
            tickets.append((start_time, end_time))
            total_coupons += 2 + abs(current_zone - Z)
            current_zone = Z
        
        # Remove expired tickets
        tickets = [(s, e) for s, e in tickets if e > T]
    
    return total_coupons

# Reading input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
trips = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

# Calculating the result
result = min_coupons(N, trips)

# Printing the result
print(result)