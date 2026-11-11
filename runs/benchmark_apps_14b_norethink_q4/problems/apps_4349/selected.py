import sys
from collections import defaultdict, deque

def min_day_to_order_microtransactions(n, m, k, offers):
    # Sort offers by day
    offers.sort()
    
    # Initialize variables
    days = 0
    burles = 0
    remaining = k[:]
    
    # Use a deque to process offers in order
    offer_index = 0
    
    while any(remaining):
        days += 1
        burles += 1
        
        # Apply offers available on this day
        while offer_index < m and offers[offer_index][0] == days:
            _, transaction_type = offers[offer_index]
            offer_index += 1
            if remaining[transaction_type - 1] > 0:
                remaining[transaction_type - 1] -= 1
                burles -= 1
        
        # Try to buy transactions with available burles
        for i in range(n):
            if remaining[i] > 0 and burles >= 2:
                remaining[i] -= 1
                burles -= 2
    
    return days

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = list(map(int, data[2:2+n]))
offers = [(int(data[2+n+2*i]), int(data[2+n+2*i+1])) for i in range(m)]

# Calculate and print the result
print(min_day_to_order_microtransactions(n, m, k, offers))