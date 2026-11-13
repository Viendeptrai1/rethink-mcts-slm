def can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    # Check if the white sheet is completely covered by the black sheets
    if x1 >= x4 or x2 <= x3 or y1 >= y4 or y2 <= y3 or x1 >= x6 or x2 <= x5 or y1 >= y6 or y2 <= y5:
        return "NO"
    else:
        return "YES"

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
x1, y1, x2, y2 = map(int, data[0:4])
x3, y3, x4, y4 = map(int, data[4:8])
x5, y5, x6, y6 = map(int, data[8:12])

# Output result
print(can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6))