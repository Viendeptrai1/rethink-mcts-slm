def can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    # Check if the white sheet is completely inside the first black sheet
    if x1 >= x3 and y1 >= y3 and x2 <= x4 and y2 <= y4:
        return False
    
    # Check if the white sheet is completely inside the second black sheet
    if x1 >= x5 and y1 >= y5 and x2 <= x6 and y2 <= y6:
        return False
    
    # Check if the white sheet overlaps with the area outside the first black sheet
    if x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3:
        return True
    
    # Check if the white sheet overlaps with the area outside the second black sheet
    if x1 < x6 and x2 > x5 and y1 < y6 and y2 > y5:
        return True
    
    # Check if the white sheet is partially visible outside both black sheets
    if (x1 < x4 or x2 > x3) and (y1 < y4 or y2 > y3) and (x1 < x6 or x2 > x5) and (y1 < y6 or y2 > y5):
        return True
    
    return False

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
x1, y1, x2, y2 = map(int, data[0:4])
x3, y3, x4, y4 = map(int, data[4:8])
x5, y5, x6, y6 = map(int, data[8:12])

# Determine if some part of the white sheet can be seen
result = "YES" if can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6) else "NO"

# Print result
print(result)