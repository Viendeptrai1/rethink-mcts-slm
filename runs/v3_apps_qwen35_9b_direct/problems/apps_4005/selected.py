import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        x1 = int(next(iterator))
        y1 = int(next(iterator))
        x2 = int(next(iterator))
        y2 = int(next(iterator))
        
        x3 = int(next(iterator))
        y3 = int(next(iterator))
        x4 = int(next(iterator))
        y4 = int(next(iterator))
        
        x5 = int(next(iterator))
        y5 = int(next(iterator))
        x6 = int(next(iterator))
        y6 = int(next(iterator))
    except StopIteration:
        return

    # White sheet
    w_x1, w_y1, w_x2, w_y2 = x1, y1, x2, y2
    
    # Black sheet 1
    b1_x1, b1_y1, b1_x2, b1_y2 = x3, y3, x4, y4
    
    # Black sheet 2
    b2_x1, b2_y1, b2_x2, b2_y2 = x5, y5, x6, y6

    # Function to calculate intersection of two rectangles
    def get_intersection(r1_x1, r1_y1, r1_x2, r1_y2, r2_x1, r2_y1, r2_x2, r2_y2):
        ix1 = max(r1_x1, r2_x1)
        iy1 = max(r1_y1, r2_y1)
        ix2 = min(r1_x2, r2_x2)
        iy2 = min(r1_y2, r2_y2)
        
        if ix1 < ix2 and iy1 < iy2:
            return (ix1, iy1, ix2, iy2)
        return None

    # Check if white is fully covered by black1
    inter1 = get_intersection(w_x1, w_y1, w_x2, w_y2, b1_x1, b1_y1, b1_x2, b1_y2)
    if inter1 is None:
        print("YES")
        return
    
    # Check if white is fully covered by black2
    inter2 = get_intersection(w_x1, w_y1, w_x2, w_y2, b2_x1, b2_y1, b2_x2, b2_y2)
    if inter2 is None:
        print("YES")
        return

    # Check if white is fully covered by the union of black1 and black2
    # This happens if:
    # 1. White is covered by black1 OR black2 individually (already checked above, but good to be explicit)
    # 2. White is covered by the intersection of (White U Black1) and Black2? No.
    # Correct logic: The union of two rectangles covers the white rectangle if:
    # The part of white NOT covered by black1 is fully covered by black2.
    # Part of white not covered by black1 = White - Intersection(White, Black1)
    # We need to check if (White - Intersection(White, Black1)) is a subset of Black2.
    # This is equivalent to: Intersection(White - Intersection(White, Black1), Black2) == (White - Intersection(White, Black1))
    # Or simpler: Is (White - Intersection(White, Black1)) empty? If yes, covered.
    # If not empty, is it fully inside Black2?
    
    # Let's compute the uncovered part by black1 relative to white.
    # The uncovered part is the set of points in White that are not in Black1.
    # Since we are dealing with axis-aligned rectangles, the difference White - Black1 might be up to 4 rectangles.
    # However, we only care if the remaining area is covered by Black2.
    
    # Alternative approach:
    # Calculate the area of White.
    # Calculate the area of (White intersect Black1).
    # Calculate the area of (White intersect Black2).
    # Calculate the area of (White intersect Black1 intersect Black2).
    # Area covered by union = Area(White n B1) + Area(White n B2) - Area(White n B1 n B2).
    # If Area covered == Area(White), then fully covered -> NO.
    # Else -> YES.
    
    def rect_area(x1, y1, x2, y2):
        return (x2 - x1) * (y2 - y1)

    area_white = rect_area(w_x1, w_y1, w_x2, w_y2)
    
    # Intersection of White and Black1
    i1 = get_intersection(w_x1, w_y1, w_x2, w_y2, b1_x1, b1_y1, b1_x2, b1_y2)
    area_i1 = rect_area(i1[0], i1[1], i1[2], i1[3]) if i1 else 0
    
    # Intersection of White and Black2
    i2 = get_intersection(w_x1, w_y1, w_x2, w_y2, b2_x1, b2_y1, b2_x2, b2_y2)
    area_i2 = rect_area(i2[0], i2[1], i2[2], i2[3]) if i2 else 0
    
    # Intersection of White, Black1, and Black2
    # First intersect White and Black1
    if i1:
        i12 = get_intersection(i1[0], i1[1], i1[2], i1[3], b2_x1, b2_y1, b2_x2, b2_y2)
    else:
        i12 = None
    area_i12 = rect_area(i12[0], i12[1], i12[2], i12[3]) if i12 else 0
    
    covered_area = area_i1 + area_i2 - area_i12
    
    if covered_area < area_white:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()