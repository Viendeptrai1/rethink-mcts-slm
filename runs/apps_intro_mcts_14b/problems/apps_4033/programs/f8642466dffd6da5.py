import sys
import math

def min_perimeter(a, b):
    # Function to find the minimum perimeter of a rectangle with given area
    def min_rect_perimeter(area):
        min_perim = float('inf')
        for i in range(1, int(math.sqrt(area)) + 1):
            if area % i == 0:
                j = area // i
                perim = 2 * (i + j)
                if perim < min_perim:
                    min_perim = perim
        return min_perim

    # Find the GCD of a and b
    gcd_ab = math.gcd(a, b)

    # The minimum perimeter is the sum of the minimum perimeters of the rectangles
    # formed by a/gcd_ab and b/gcd_ab
    return min_rect_perimeter(a // gcd_ab) + min_rect_perimeter(b // gcd_ab)

# Read input
a, b = map(int, sys.stdin.read().split())

# Calculate and print the result
print(min_perimeter(a, b))