def can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    # Check if a point (px, py) is strictly inside a rectangle defined by (lx, ly, rx, ry)
    def is_strictly_inside(px, py, lx, ly, rx, ry):
        return lx < px < rx and ly < py < ry

    # Check if a point (px, py) is strictly outside a rectangle defined by (lx, ly, rx, ry)
    def is_strictly_outside(px, py, lx, ly, rx, ry):
        return px < lx or px > rx or py < ly or py > ry

    # Check if the white sheet is strictly outside both black sheets
    def is_white_outside_black_sheets(px, py):
        return (is_strictly_outside(px, py, x3, y3, x4, y4) and
                is_strictly_outside(px, py, x5, y5, x6, y6))

    # Check points on the edges of the white sheet
    for px in [x1, x2]:
        for py in range(y1, y2 + 1):
            if is_white_outside_black_sheets(px, py):
                return "YES"

    for py in [y1, y2]:
        for px in range(x1, x2 + 1):
            if is_white_outside_black_sheets(px, py):
                return "YES"

    # Check points on the corners of the white sheet
    corners = [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
    for px, py in corners:
        if is_white_outside_black_sheets(px, py):
            return "YES"

    return "NO"

# Read input
x1, y1, x2, y2 = map(int, input().split())
x3, y3, x4, y4 = map(int, input().split())
x5, y5, x6, y6 = map(int, input().split())

# Output result
print(can_see_white_sheet(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6))