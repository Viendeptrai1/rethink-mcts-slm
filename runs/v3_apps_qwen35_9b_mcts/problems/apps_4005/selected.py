import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    def get_int():
        return int(next(iterator))

    x1, y1, x2, y2 = get_int(), get_int(), get_int(), get_int()
    x3, y3, x4, y4 = get_int(), get_int(), get_int(), get_int()
    x5, y5, x6, y6 = get_int(), get_int(), get_int(), get_int()

    def intersect_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
        # Calculate intersection rectangle
        ix1 = max(ax1, bx1)
        iy1 = max(ay1, by1)
        ix2 = min(ax2, bx2)
        iy2 = min(ay2, by2)
        
        if ix1 >= ix2 or iy1 >= iy2:
            return 0
        return (ix2 - ix1) * (iy2 - iy1)

    white_area = (x2 - x1) * (y2 - y1)
    
    # Area covered by black1 within white
    area1 = intersect_area(x1, y1, x2, y2, x3, y3, x4, y4)
    
    # Area covered by black2 within white
    area2 = intersect_area(x1, y1, x2, y2, x5, y5, x6, y6)
    
    # Area covered by both black sheets within white (intersection of black1 and black2, then intersect with white)
    # First find intersection of black1 and black2
    bx1, by1, bx2, by2 = max(x3, x5), max(y3, y5), min(x4, x6), min(y4, y6)
    if bx1 < bx2 and by1 < by2:
        area_both = intersect_area(x1, y1, x2, y2, bx1, by1, bx2, by2)
    else:
        area_both = 0

    covered_area = area1 + area2 - area_both

    if covered_area < white_area:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()