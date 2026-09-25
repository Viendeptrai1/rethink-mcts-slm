import sys
from sortedcontainers import SortedList

def count_median_pairs(n, m, p):
    # Initialize variables
    count = 0
    balance = 0
    prefix_count = {0: 1}
    
    # Create a sorted list to keep track of elements less than m
    less_than_m = SortedList()
    
    for i in range(n):
        if p[i] < m:
            less_than_m.add(p[i])
            balance += 1
        elif p[i] > m:
            balance -= 1
        
        # Calculate the number of valid subarrays ending at index i
        if balance >= 0:
            count += prefix_count.get(balance, 0)
            count += prefix_count.get(balance - 1, 0)
        else:
            count += prefix_count.get(-balance, 0)
            count += prefix_count.get(-balance + 1, 0)
        
        # Update the prefix count
        prefix_count[balance] = prefix_count.get(balance, 0) + 1
    
    return count

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
p = list(map(int, data[2:]))

# Output the result
print(count_median_pairs(n, m, p))