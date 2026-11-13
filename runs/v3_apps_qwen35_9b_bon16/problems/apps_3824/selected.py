import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    x1 = int(input_data[0])
    y1 = int(input_data[1])
    x2 = int(input_data[2])
    y2 = int(input_data[3])

    # Calculate Manhattan distance between start and flag
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    # If the start and flag are on the same row or same column, we need to take a detour
    # to form a closed loop around the flag.
    # The minimal loop will essentially go from start to flag, go around it, and come back.
    #
    # Case 1: Start and Flag are on the same row (dy == 0)
    # We must go at least 1 step away from the row, circle the flag, and return.
    # Path: (x1,y1) -> ... -> (x2, y1+1) -> (x2+1, y1+1) -> ... -> (x2+1, y1-1) -> ... -> (x1, y1-1) -> ... -> (x1,y1)
    # Actually, the most efficient way is to form a rectangle that includes the flag strictly inside.
    # The bounding box of the path must contain the flag (x2, y2) in its interior.
    # So the path x-range must be at least [min(x1,x2)-1, max(x1,x2)+1] ? No.
    # The flag must be strictly inside.
    # Let the path define a bounding box [X_min, X_max] x [Y_min, Y_max].
    # For (x2, y2) to be strictly inside, we need X_min < x2 < X_max and Y_min < y2 < Y_max.
    # Also, the path must start at (x1, y1), so (x1, y1) must be on the boundary of this box (or reachable via the boundary).
    # Actually, the path is a cycle. The minimal perimeter rectangle containing (x2,y2) strictly inside
    # with (x1,y1) on its boundary is the solution.
    #
    # Let's derive the dimensions.
    # We need X_min <= min(x1, x2) - 1 ? Not necessarily.
    # If x1 < x2: we need X_min < x2 and X_max > x2. Since x1 is on the path, x1 >= X_min and x1 <= X_max.
    # To minimize perimeter, we want the box to be as small as possible.
    # Constraints:
    # 1. X_min < x2 < X_max
    # 2. Y_min < y2 < Y_max
    # 3. (x1, y1) is on the perimeter: x1=X_min or x1=X_max or y1=Y_min or y1=Y_max.
    #
    # Let's consider the distance in X and Y.
    # dx = |x1 - x2|, dy = |y1 - y2|
    #
    # If dx == 0 and dy == 0: Not possible per problem statement.
    #
    # If dx == 0 (same column):
    #   We need to shift horizontally by at least 1 unit from x1 to enclose x2 (since x2=x1).
    #   So the width of the box must be at least 2 (from x1-1 to x1+1).
    #   The height must cover y1 and allow y2 to be strictly inside.
    #   Since y2 is on the line segment between y1 and itself (just y2), we need Y_min < y2 < Y_max.
    #   And y1 must be on the boundary.
    #   Minimal box:
    #     X range: [x1-1, x1+1] (width 2). Perimeter contribution 2*2 = 4.
    #     Y range: We need to go from y1 to y2 and surround.
    #     If we just take the segment [min(y1,y2), max(y1,y2)], y2 is on the boundary, not strictly inside.
    #     So we need to extend Y by at least 1 in one direction or both?
    #     To make y2 strictly inside, we need Y_min <= y2-1 and Y_max >= y2+1.
    #     Also y1 must be <= Y_min or y1 >= Y_max or y1 is between (but on horizontal sides).
    #     Actually, if x1=x2, the only way to strictly enclose (x1,y2) is to have x range [x1-1, x1+1].
    #     Then for y, we need a vertical span such that y2 is strictly inside.
    #     The path goes up and down.
    #     Minimal Y range: [min(y1, y2)-1, max(y1, y2)+1]? 
    #     Let's test with example: (0,1) to (0,0). dx=0, dy=1.
    #     x range: [-1, 1].
    #     y range: need 0 strictly inside. So y_min <= -1, y_max >= 1.
    #     We must include (0,1). So y_max >= 1.
    #     If we pick y_min = -1, y_max = 1. Box: [-1,1]x[-1,1].
    #     Is (0,0) strictly inside? Yes (-1<0<1 and -1<0<1).
    #     Is (0,1) on boundary? Yes (y=1).
    #     Perimeter = 2*(width + height) = 2*(2 + 2) = 8. Matches example 2.
    #     Formula for dx=0: width = 2. Height = dy + 2? 
    #     Here dy=1, height=2. 1+2=3? No, height is 2.
    #     Let's re-evaluate height.
    #     We need interval [A, B] such that A < y2 < B and y1 is in [A, B] and on boundary.
    #     Minimal length B-A?
    #     If y1 > y2: we can set B = y1. Then we need A <= y2-1. So A = y2-1.
    #       Height = y1 - (y2-1) = (y1-y2) + 1 = dy + 1.
    #     If y1 < y2: we can set A = y1. Then we need B >= y2+1. So B = y2+1.
    #       Height = (y2+1) - y1 = (y2-y1) + 1 = dy + 1.
    #     Wait, in the example (0,1) to (0,0): y1=1, y2=0. y1 > y2.
    #     B = 1. A = 0-1 = -1. Height = 1 - (-1) = 2. dy = 1. Height = dy + 1.
    #     But earlier I said height=2. Correct.
    #     Perimeter = 2 * (2 + dy + 1) = 2 * (dy + 3) = 2*dy + 6.
    #     For dy=1: 2+6=8. Correct.
    #
    # If dy == 0 (same row):
    #   Symmetric to above. Width = dy + 1? No, width = dx + 1. Height = 2.
    #   Perimeter = 2 * (dx + 1 + 2) = 2 * (dx + 3) = 2*dx + 6.
    #
    # If dx > 0 and dy > 0 (diagonal):
    #   We need X_min < x2 < X_max and Y_min < y2 < Y_max.
    #   And (x1, y1) on boundary.
    #   Minimal box:
    #     X range: [min(x1, x2), max(x1, x2)]?
    #     If we use [min(x1,x2), max(x1,x2)], then one of x1 or x2 is on the boundary x=min or x=max.
    #     But we need x2 strictly inside, so x_min < x2 < x_max.
    #     If x1 < x2: x_min must be <= x1. x_max must be >= x2+1.
    #       Minimal: x_min = x1, x_max = x2+1. Width = (x2+1) - x1 = dx + 1.
    #     If x1 > x2: x_min = x2-1, x_max = x1. Width = x1 - (x2-1) = dx + 1.
    #     Similarly for Y:
    #       If y1 < y2: y_min = y1, y_max = y2+1. Height = dy + 1.
    #       If y1 > y2: y_min = y2-1, y_max = y1. Height = dy + 1.
    #     So Width = dx + 1, Height = dy + 1.
    #     Perimeter = 2 * (dx + 1 + dy + 1) = 2 * (dx + dy + 2) = 2*dx + 2*dy + 4.
    #     Let's check example 1: (1,5) to (5,2).
    #     dx = 4, dy = 3.
    #     Perimeter = 2*4 + 2*3 + 4 = 8 + 6 + 4 = 18. Matches example 1.
    #
    # Summary:
    # If dx == 0: ans = 2 * (2 + dy + 1) = 2*dy + 6
    # If dy == 0: ans = 2 * (dx + 1 + 2) = 2*dx + 6
    # If dx > 0 and dy > 0: ans = 2 * (dx + dy + 2) = 2*dx + 2*dy + 4
    #
    # Can we unify?
    # Case 1: dx=0. Formula 2*dx + 2*dy + 4 would give 2*dy+4. But we need 2*dy+6. Diff is 2.
    # Case 2: dy=0. Formula 2*dx + 2*dy + 4 would give 2*dx+4. But we need 2*dx+6. Diff is 2.
    # Case 3: both > 0. Formula works.
    #
    # Why the difference?
    # When dx=0, we force width=2 (fixed), but the standard "diagonal" logic would try to set width = dx+1 = 1.
    # But width must be at least 2 to enclose x2 strictly (since x1=x2).
    # So effective width = max(dx+1, 2).
    # Effective height = max(dy+1, 2).
    # Then Perimeter = 2 * (effective_width + effective_height).
    #
    # Let's verify:
    # dx=0, dy=1. eff_w = max(1, 2)=2. eff_h = max(2, 2)=2. P = 2*(2+2)=8. Correct.
    # dx=4, dy=3. eff_w = max(5, 2)=5. eff_h = max(4, 2)=4. P = 2*(5+4)=18. Correct.
    # dx=0, dy=0 (impossible).
    #
    # Logic holds.

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    w = dx + 1
    h = dy + 1

    # Ensure minimum dimensions to strictly enclose
    if w < 2:
        w = 2
    if h < 2:
        h = 2

    print(2 * (w + h))

if __name__ == "__main__":
    solve()