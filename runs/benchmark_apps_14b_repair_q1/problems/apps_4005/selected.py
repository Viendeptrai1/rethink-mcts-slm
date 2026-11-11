def is_visible(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    # Function to check if a point (px, py) is covered by a black sheet
    def is_covered(px, py, bx1, by1, bx2, by2):
        return bx1 <= px <= bx2 and by1 <= py <= by2
    
    # Check all boundary points of the white sheet
    for px in [x1, x2]:
        for py in range(y1, y2 + 1):
            if not is_covered(px, py, x3, y3, x4, y4) and not is_covered(px, py, x5, y5, x6, y6):
                return "YES"
    
    for py in [y1, y2]:
        for px in range(x1, x2 + 1):
            if not is_covered(px, py, x3, y3, x4, y4) and not is_covered(px, py, x5, y5, x6, y6):
                return "YES"
    
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()

x1, y1, x2, y2 = map(int, data[:4])
x3, y3, x4, y4 = map(int, data[4:8])
x5, y5, x6, y6 = map(int, data[8:])

# Determine if some part of the white sheet can be seen
result = is_visible(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6)

# Print the result
print(result)