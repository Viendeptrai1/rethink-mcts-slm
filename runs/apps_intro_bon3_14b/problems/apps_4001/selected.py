import sys
from collections import Counter

def find_x_y(n, divisors):
    # Count the frequency of each divisor
    freq = Counter(divisors)
    
    # Find the maximum divisor which appears exactly twice
    max_common_divisor = None
    for divisor, count in freq.items():
        if count == 2:
            if max_common_divisor is None or divisor > max_common_divisor:
                max_common_divisor = divisor
    
    # The maximum common divisor must be present in both x and y
    # Remove it from the frequency counter
    freq[max_common_divisor] -= 2
    
    # Now, we need to split the remaining divisors into two sets
    # One set will be the divisors of x and the other will be the divisors of y
    x_divisors = set()
    y_divisors = set()
    
    for divisor, count in freq.items():
        if count == 1:
            if divisor % max_common_divisor == 0:
                x_divisors.add(divisor)
            else:
                y_divisors.add(divisor)
    
    # Calculate x and y
    x = max_common_divisor
    for divisor in x_divisors:
        x *= divisor
    
    y = max_common_divisor
    for divisor in y_divisors:
        y *= divisor
    
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