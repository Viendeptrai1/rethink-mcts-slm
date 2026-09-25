import sys
from math import gcd

def min_perimeter(a, b):
    # Calculate the greatest common divisor of a and b
    g = gcd(a, b)
    
    # Calculate the minimum perimeter
    min_p = 2 * (a // g + b // g)
    
    return min_p

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])

# Calculate and print the result
result = min_perimeter(a, b)
print(result)