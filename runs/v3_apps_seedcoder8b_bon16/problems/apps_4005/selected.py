def can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    def is_point_outside_sheets(px, py):
        # Check if point (px, py) is strictly outside all sheets
        return ((px <= x1 or px >= x2) or 
                (py <= y1 or py >= y2) or 
                (x3 <= px < x4 and y3 <= py < y4) or 
                (x5 <= px < x6 and y5 <= py < y6))
    
    # Check if there's any point outside white sheet which is inside neither black sheet
    for px in range(x1, x2 + 1):
        for py in range(y1, y2 + 1):
            if (px > x1 and px < x2 and py > y1 and py < y2 and
                not (x3 <= px < x4 and y3 <= py < y4) and
                not (x5 <= px < x6 and y5 <= py < y6)):
                # There's a point inside white sheet but outside both black sheets
                return "YES"
    return "NO"

# Read input
x1, y1, x2, y2 = map(int, input().split())
x3, y3, x4, y4 = map(int, input().split())
x5, y5, x6, y6 = map(int, input().split())

# Compute and print result
print(can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6))