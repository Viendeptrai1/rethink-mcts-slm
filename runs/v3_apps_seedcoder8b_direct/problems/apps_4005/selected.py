def can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    def is_inside(x, y, x_min, y_min, x_max, y_max):
        return x_min < x < x_max and y_min < y < y_max

    def is_outside(x, y, x_min, y_min, x_max, y_max):
        return x <= x_min or x >= x_max or y <= y_min or y >= y_max

    # Check if any point on the boundary of the white sheet is not inside any black sheet
    for x in [x1, x2]:
        for y in [y1, y2]:
            if is_outside(x, y, x3, y3, x4, y4) and is_outside(x, y, x5, y5, x6, y6):
                return "YES"

    # Check if any point on the boundary of the black sheets is not inside the white sheet
    for x in [x3, x4, x5, x6]:
        for y in [y3, y4, y5, y6]:
            if is_outside(x, y, x1, y1, x2, y2):
                return "YES"

    # Check if there is any point inside the white sheet that is not inside any black sheet
    for x in range(x1 + 1, x2):
        for y in range(y1 + 1, y2):
            if is_outside(x, y, x3, y3, x4, y4) and is_outside(x, y, x5, y5, x6, y6):
                return "YES"

    return "NO"

# Read input
x1, y1, x2, y2 = map(int, input().split())
x3, y3, x4, y4 = map(int, input().split())
x5, y5, x6, y6 = map(int, input().split())

# Print result
print(can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6))