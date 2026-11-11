import sys
from math import ceil, log

def find_smallest_n(m):
    if m == 1:
        return 8
    
    # We need to find the smallest n such that the number of ways to distribute chocolates
    # among 4 thieves with a ratio k is exactly m.
    # The number of ways is given by the sum of divisors of n-1.
    
    # Function to count the number of divisors of a number
    def count_divisors(x):
        count = 0
        for i in range(1, int(x**0.5) + 1):
            if x % i == 0:
                count += 1
                if i != x // i:
                    count += 1
        return count
    
    # Start checking from the smallest possible n
    n = 9  # Since n must be at least 9 to have 4 thieves taking chocolates
    while True:
        if count_divisors(n - 1) == m:
            return n
        n += 1

# Read input
m = int(sys.stdin.read().strip())

# Find and print the result
result = find_smallest_n(m)
print(result)