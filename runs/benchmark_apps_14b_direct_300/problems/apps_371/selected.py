import sys
from math import log, ceil

def find_smallest_n(m):
    if m == 1:
        return 8
    
    # We need to find the smallest n such that the number of ways to distribute chocolates is exactly m
    # The number of ways is given by the number of solutions to the equation x + kx + k^2x + k^3x <= n
    # This simplifies to x(1 + k + k^2 + k^3) <= n
    # We need to find the smallest n for which there are exactly m solutions for x
    
    # The number of solutions for x is given by floor(n / (1 + k + k^2 + k^3))
    # We need to find the smallest n such that this expression equals m
    
    # Let's iterate over possible values of k starting from 2
    for k in range(2, 1000):  # Arbitrarily large upper limit for k
        sum_k = 1 + k + k**2 + k**3
        # We need to find the smallest n such that floor(n / sum_k) = m
        # This means n must be in the range [m * sum_k, (m + 1) * sum_k - 1]
        n_min = m * sum_k
        n_max = (m + 1) * sum_k - 1
        
        # Check if there exists an n in this range that satisfies the condition
        if n_min <= n_max:
            return n_min
    
    return -1

# Read input
m = int(sys.stdin.read().strip())

# Find and print the smallest n
print(find_smallest_n(m))