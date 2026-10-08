def is_visible(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    def overlap_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
        dx = min(ax2, bx2) - max(ax1, bx1)
        dy = min(ay2, by2) - max(ay1, by1)
        return max(dx, 0) * max(dy, 0)

    # Calculate the area of the white sheet
    white_area = (x2 - x1) * (y2 - y1)

    # Calculate the overlapping areas with each black sheet
    overlap1 = overlap_area(x1, y1, x2, y2, x3, y3, x4, y4)
    overlap2 = overlap_area(x1, y1, x2, y2, x5, y5, x6, y6)

    # Calculate the total overlapping area
    total_overlap = overlap1 + overlap2

    # Check if there is any part of the white sheet visible
    if white_area > total_overlap:
        return "YES"
    else:
        return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()

x1, y1, x2, y2 = map(int, data[:4])
x3, y3, x4, y4 = map(int, data[4:8])
x5, y5, x6, y6 = map(int, data[8:])

# Output the result
print(is_visible(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6))