import sys
from math import sqrt
from collections import Counter

def find_x_y(n, divisors):
    # Calculate the product of all divisors
    product = 1
    for d in divisors:
        product *= d
    
    # The LCM of x and y is the square root of the product
    lcm_xy = int(sqrt(product))
    
    # Count the occurrences of each divisor
    divisor_count = Counter(divisors)
    
    # Find the greatest common divisor (GCD) of x and y
    gcd_xy = 1
    for d in divisor_count:
        if divisor_count[d] == 2:
            gcd_xy *= d
    
    # Calculate x and y using the relationships between GCD, LCM, and product
    x = gcd_xy * (lcm_xy // gcd_xy)
    y = lcm_xy
    
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