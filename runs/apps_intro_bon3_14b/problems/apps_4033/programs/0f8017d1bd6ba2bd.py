import sys
import math

def min_perimeter(a, b):
    # Function to find the minimum perimeter of a rectangle with area n
    def min_rectangle_perimeter(n):
        min_perim = float('inf')
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                j = n // i
                min_perim = min(min_perim, 2 * (i + j))
        return min_perim

    # Calculate the total number of tiles
    total_tiles = a + b

    # Find the minimum perimeter of a rectangle with area a
    min_red_perim = min_rectangle_perimeter(a)

    # Find the minimum perimeter of a rectangle with area b
    min_blue_perim = min_rectangle_perimeter(b)

    # Find the minimum perimeter of a rectangle with area total_tiles
    min_total_perim = min_rectangle_perimeter(total_tiles)

    # The answer is the minimum of the above three perimeters
    return min(min_red_perim, min_blue_perim, min_total_perim)

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])

# Calculate and print the result
result = min_perimeter(a, b)
print(result)