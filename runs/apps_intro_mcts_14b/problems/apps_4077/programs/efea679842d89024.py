import sys
from collections import defaultdict

def count_median_subarrays(n, m, a):
    # Initialize variables
    count = 0
    less_count = 0
    equal_count = 0
    greater_count = 0
    
    # Dictionary to store the difference between counts of elements less than and equal to m
    diff_count = defaultdict(int)
    diff_count[0] = 1
    
    # Iterate through the array
    for i in range(n):
        if a[i] < m:
            less_count += 1
        elif a[i] == m:
            equal_count += 1
        else:
            greater_count += 1
        
        # Calculate the current difference
        current_diff = less_count - equal_count
        
        # Check for valid subarrays ending at index i
        if current_diff <= 0:
            count += diff_count[current_diff]
        
        # Update the dictionary with the current difference
        diff_count[current_diff] += 1
    
    return count

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(count_median_subarrays(n, m, a))