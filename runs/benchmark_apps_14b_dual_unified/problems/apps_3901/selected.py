import sys
from math import gcd
from functools import reduce

def min_operations_to_one(n, a):
    # Check if the GCD of the entire array is 1
    overall_gcd = reduce(gcd, a)
    if overall_gcd != 1:
        return -1
    
    # Count the number of elements that are already 1
    count_ones = a.count(1)
    
    # The minimum number of operations needed is the total number of elements minus the number of 1s
    return n - count_ones

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Print the result
print(min_operations_to_one(n, a))