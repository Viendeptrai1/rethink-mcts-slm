def min_path(x1, y1, x2, y2):
    # Calculate the Manhattan distance from the starting point to the flag
    dist_to_flag = abs(x1 - x2) + abs(y1 - y2)
    # The minimum path length is twice the distance to the flag plus 2 (to form a loop)
    return 2 * dist_to_flag + 2

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
x1, y1 = int(data[0]), int(data[1])
x2, y2 = int(data[2]), int(data[3])

# Calculate and print the result
print(min_path(x1, y1, x2, y2))