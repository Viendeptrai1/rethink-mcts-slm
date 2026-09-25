import sys
from math import gcd

def min_perimeter(a, b):
    total_tiles = a + b
    common_divisor = gcd(a, b)
    
    # Find the dimensions of the smallest rectangle that can contain both a and b tiles
    width = total_tiles // common_divisor
    height = common_divisor
    
    # Calculate the perimeter of this rectangle
    perimeter = 2 * (width + height)
    return perimeter

# Read input
input_line = sys.stdin.read().strip()
a, b = map(int, input_line.split())

# Output the result
print(min_perimeter(a, b))