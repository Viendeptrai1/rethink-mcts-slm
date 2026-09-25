import sys
import math

def min_perimeter(a, b):
    # Function to find the minimum perimeter of the rectangle
    def find_min_perimeter(x, y):
        min_p = float('inf')
        # Iterate over all possible factors of x
        for i in range(1, int(math.sqrt(x)) + 1):
            if x % i == 0:
                j = x // i
                # Check if y can be formed with the remaining dimensions
                if (y % j == 0 and i + j <= x + y) or (y % i == 0 and j + i <= x + y):
                    min_p = min(min_p, 2 * (i + j))
        return min_p

    # Calculate the minimum perimeter for the given a and b
    return min(find_min_perimeter(a, b), find_min_perimeter(b, a))

# Read input
a, b = map(int, sys.stdin.read().split())

# Print the result
print(min_perimeter(a, b))