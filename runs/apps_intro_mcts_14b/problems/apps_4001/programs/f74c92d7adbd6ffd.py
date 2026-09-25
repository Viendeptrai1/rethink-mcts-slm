import sys
from collections import Counter
from math import gcd

def find_x_y(n, divisors):
    # Count the frequency of each divisor
    count = Counter(divisors)
    
    # Find all divisors that appear exactly twice
    potential_gcds = [d for d, c in count.items() if c == 2]
    
    # The GCD must be the greatest common divisor of these potential GCDs
    actual_gcd = potential_gcds[0]
    for d in potential_gcds[1:]:
        actual_gcd = gcd(actual_gcd, d)
    
    # Now we know the GCD, we can partition the divisors
    divisors_of_x = set()
    divisors_of_y = set()
    
    for d in divisors:
        if d % actual_gcd == 0:
            divisors_of_x.add(d)
        else:
            divisors_of_y.add(d)
    
    # The product of all divisors of x divided by the GCD is x itself
    x = 1
    for d in divisors_of_x:
        x *= d // actual_gcd
    
    # Similarly for y
    y = 1
    for d in divisors_of_y:
        y *= d // actual_gcd
    
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