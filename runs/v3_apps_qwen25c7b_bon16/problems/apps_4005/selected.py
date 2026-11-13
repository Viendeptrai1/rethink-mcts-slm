def can_be_seen(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    # Check if the white sheet is completely within the bounds of either black sheet
    if x1 >= x3 and x2 <= x4 and y1 >= y3 and y2 <= y4 or \
       x1 >= x5 and x2 <= x6 and y1 >= y5 and y2 <= y6:
        return "NO"
    
    # Check if the white sheet intersects with either black sheet
    if x2 > x3 and x1 < x4 and y2 > y3 and y1 < y4 or \
       x2 > x5 and x1 < x6 and y2 > y5 and y1 < y6:
        return "YES"
    
    # Check if any edge of the white sheet is outside both black sheets
    if x1 <= x3 and x1 >= x5 and y1 <= y3 and y1 >= y5 and x2 <= x6 and y2 <= y4 and y2 >= y5:
        return "YES"
    if x2 >= x3 and x2 <= x5 and y1 <= y3 and y1 >= y5 and x1 >= x3 and y2 <= y4 and y2 >= y5:
        return "YES"
    if x1 <= x3 and x1 >= x5 and y2 >= y3 and y2 <= y6 and x2 <= x4 and y1 >= y3 and y1 <= y6:
        return "YES"
    if x2 >= x3 and x2 <= x5 and y2 >= y3 and y2 <= y6 and x1 >= x3 and y1 >= y3 and y1 <= y6:
        return "YES"
    
    # If none of the above conditions are met, it means some part of the white sheet can be seen
    return "YES"

# Read input
import sys
input = sys.stdin.read
data = input().split()

x1, y1, x2, y2 = map(int, data[0:4])
x3, y3, x4, y4 = map(int, data[4:8])
x5, y5, x6, y6 = map(int, data[8:])

# Output result
print(can_be_seen(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6))