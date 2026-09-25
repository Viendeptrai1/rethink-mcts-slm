import sys
from collections import Counter
from math import gcd

def find_x_y(n, divisors):
    # Count the frequency of each divisor
    count = Counter(divisors)
    
    # Find the GCD of all divisors
    g = divisors[0]
    for d in divisors:
        g = gcd(g, d)
    
    # Remove the GCD from the count as it will be part of both x and y
    count[g] -= 2
    
    # Initialize x and y with the GCD
    x = g
    y = g
    
    # Distribute the remaining divisors
    for d in divisors:
        if count[d] > 0:
            if x % d == 0:
                x *= d
            else:
                y *= d
            count[d] -= 1
    
    return x, y

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
divisors = list(map(int, data[1:]))

# Find x and y
x, y = find_x_y(n, divisors)

# Print the result
print(x, y)