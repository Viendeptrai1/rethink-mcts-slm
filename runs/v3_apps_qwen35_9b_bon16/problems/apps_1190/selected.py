import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    w1 = int(input_data[0])
    h1 = int(input_data[1])
    w2 = int(input_data[2])
    h2 = int(input_data[3])
    
    # The shape is composed of two rectangles stacked vertically and left-aligned.
    # Rectangle 1 (bottom): width w1, height h1. Covers x in [1, w1], y in [1, h1].
    # Rectangle 2 (top): width w2, height h2. Covers x in [1, w2], y in [h1+1, h1+h2].
    # We need to count the number of empty cells that share at least one corner or side 
    # with any cell of the ship. This is equivalent to the area of the bounding box of 
    # the union of the ship and its 8-neighbors, minus the area of the ship itself, 
    # plus any adjustments if the "neighbor zone" wraps around concave corners differently.
    # 
    # Actually, a simpler geometric approach:
    # The set of marked cells is the set of points (x, y) such that the distance (Chebyshev) 
    # from (x, y) to the ship is <= 1, excluding points inside the ship.
    # 
    # Let's calculate the bounding box of the entire structure (ship + 1-cell padding).
    # Min X = 0 (since ship starts at 1, padding goes to 0)
    # Max X = w1 + 1 (since ship ends at w1, padding goes to w1+1)
    # Min Y = 0 (since ship starts at 1, padding goes to 0)
    # Max Y = h1 + h2 + 1 (since ship ends at h1+h2, padding goes to h1+h2+1)
    #
    # The bounding box of the marked cells plus the ship is from (0,0) to (w1+1, h1+h2+1).
    # Total area of this bounding box = (w1 + 1) * (h1 + h2 + 1).
    #
    # However, this bounding box might include some "holes" or non-marked areas if the shape 
    # is not convex. But here, the shape is L-like or rectangular.
    # The union of the ship and its neighbors forms a shape that is essentially the bounding box 
    # MINUS the corners that are "inside" the concavity of the shape but outside the bounding box logic?
    # No, let's re-evaluate.
    #
    # Consider the concave corner.
    # If w2 < w1 and h2 > 0 and h1 > 0:
    # The ship looks like an inverted 'L' if we consider the missing top-right part of the bottom rectangle.
    # Actually, the bottom rect is wide (w1), top rect is narrow (w2) and sits on top left.
    # So the "missing" part relative to a full rectangle of width w1 and height h1+h2 is the region:
    # x in [w2+1, w1], y in [h1+1, h1+h2].
    #
    # The marked cells surround the ship.
    # Let's count directly by cases or use the bounding box method with correction.
    #
    # Bounding box of the ship: x in [1, w1], y in [1, h1+h2].
    # Width = w1, Height = h1+h2.
    #
    # The "neighborhood" expands this box by 1 in all directions:
    # x in [0, w1+1], y in [0, h1+h2+1].
    # Area of this expanded box = (w1+1) * (h1+h2+1).
    #
    # Does this expanded box contain any cells that are NOT neighbors?
    # The only potential issue is the "inner corner" of the L-shape.
    # The ship occupies:
    #   R1: [1, w1] x [1, h1]
    #   R2: [1, w2] x [h1+1, h1+h2]
    #
    # The expanded box covers:
    #   [0, w1+1] x [0, h1+h2+1]
    #
    # Let's check the region corresponding to the "concave" part: x in [w2+1, w1], y in [h1+1, h1+h2].
    # This region is EMPTY of ship.
    # Are these cells marked?
    # A cell (x, y) in this region is marked if it is adjacent (side or corner) to the ship.
    # Adjacent to R1? The top of R1 is y=h1. This region starts at y=h1+1.
    #   Cells in this region have y >= h1+1. The closest part of R1 is at y=h1.
    #   For a cell (x, h1+1) where w2 < x <= w1:
    #     It is directly above R1? No, R1 goes up to h1. So (x, h1+1) is adjacent to (x, h1) which is in R1.
    #     So the entire bottom edge of this empty region touches R1. Thus, the row y=h1+1 for x in [w2+1, w1] is marked.
    #   What about y > h1+1?
    #     These cells are above the empty space. Are they adjacent to anything?
    #     They are not adjacent to R1 (distance > 1 vertically).
    #     They are not adjacent to R2 (R2 is only up to x=w2, so for x > w2, there is no horizontal overlap).
    #     Therefore, cells with y > h1+1 and w2 < x <= w1 are NOT adjacent to the ship.
    #
    # So, the expanded box includes a rectangular region of non-marked cells:
    #   x in [w2+1, w1], y in [h1+2, h1+h2+1] (if h2 >= 1)
    #   Wait, let's re-check the boundary.
    #   The ship's top is at h1+h2. The neighbor zone goes to h1+h2+1.
    #   The empty region in the bounding box is x in [w2+1, w1] and y in [h1+1, h1+h2+1].
    #   The row y=h1+1 is adjacent to R1 (at y=h1), so it IS marked.
    #   The rows y from h1+2 to h1+h2+1 are NOT adjacent to R1 (too far) and NOT adjacent to R2 (x too large).
    #   So the non-marked area inside the bounding box is:
    #     Width = w1 - w2
    #     Height = (h1+h2+1) - (h1+1) = h2? No.
    #     Range of y for non-marked: [h1+2, h1+h2+1].
    #     Count = (h1+h2+1) - (h1+2) + 1 = h2.
    #     Wait, if h2=1, range is [h1+2, h1+2]. Count = 1. Formula h2 gives 1. Correct.
    #     If h2=0? The problem says h2 >= 1.
    #
    # So, Total Marked = Area(Expanded Box) - Area(Ship) - Area(Unmarked inside Box)
    # Area(Expanded Box) = (w1 + 1) * (h1 + h2 + 1)
    # Area(Ship) = w1*h1 + w2*h2
    # Area(Unmarked) = (w1 - w2) * h2  <-- Wait, let's re-verify the height.
    #   The unmarked region is x in [w2+1, w1] and y in [h1+2, h1+h2+1].
    #   Number of x's = w1 - w2.
    #   Number of y's = (h1+h2+1) - (h1+2) + 1 = h2.
    #   Yes, height is h2.
    #
    # So Answer = (w1 + 1)(h1 + h2 + 1) - (w1*h1 + w2*h2) - (w1 - w2)*h2
    #
    # Let's simplify:
    # Ans = (w1 + 1)(h1 + h2 + 1) - w1*h1 - w2*h2 - (w1*h2 - w2*h2)
    # Ans = w1*h1 + w1*h2 + w1 + h1 + h2 + 1 - w1*h1 - w2*h2 - w1*h2 + w2*h2
    # Ans = w1 + h1 + h2 + 1
    #
    # WAIT. This result (w1 + h1 + h2 + 1) seems too small.
    # Let's test with Example 1: w1=2, h1=1, w2=2, h2=1.
    # Ship: 2x1 (bottom), 2x1 (top). Total shape is 2x2 square.
    # Neighbors of a 2x2 square:
    # Perimeter is 8 cells. Corners add 4 more?
    # Bounding box of ship: x[1,2], y[1,2]. Area=4.
    # Expanded box: x[0,3], y[0,3]. Area=16.
    # Unmarked inside expanded box?
    # Since w2=w1=2, the "concave" part width w1-w2 = 0. So no unmarked region inside.
    # Formula: 16 - 4 - 0 = 12.
    # My simplified formula: w1 + h1 + h2 + 1 = 2 + 1 + 1 + 1 = 5. Incorrect.
    # Where did I go wrong?
    # Ah, the simplification:
    # (w1 + 1)(h1 + h2 + 1) = w1*h1 + w1*h2 + w1 + h1 + h2 + 1.
    # Subtract Ship (w1*h1 + w2*h2).
    # Subtract Unmarked ((w1-w2)*h2).
    # Result = w1*h1 + w1*h2 + w1 + h1 + h2 + 1 - w1*h1 - w2*h2 - w1*h2 + w2*h2
    # The terms w1*h2 and -w1*h2 cancel.
    # The terms -w2*h2 and +w2*h2 cancel.
    # Left with: w1 + h1 + h2 + 1.
    # Why is this wrong for the 2x2 square?
    # For 2x2 square (w1=2, h1=1, w2=2, h2=1):
    # Expanded box area = 3 * 3 = 9. (Not 16).
    # My previous calculation of expanded box was (w1+1)*(h1+h2+1) = 3 * 3 = 9.
    # Ship area = 4.
    # Unmarked = 0.
    # Result = 9 - 4 = 5.
    # BUT the example output is 12.
    # Why?
    # "All cells neighboring by side or a corner with the ship are marked."
    # If the ship is a 2x2 square at (1,1) to (2,2).
    # Neighbors:
    # y=0: (0,0), (1,0), (2,0), (3,0) -> 4 cells.
    # y=1: (0,1), (3,1) -> 2 cells (sides). (1,1),(2,1) are ship.
    # y=2: (0,2), (3,2) -> 2 cells.
    # y=3: (0,3), (1,3), (2,3), (3,3) -> 4 cells.
    # Total = 4 + 2 + 2 + 4 = 12.
    #
    # My expanded box logic:
    # Ship x: 1..2, y: 1..2.
    # Expanded x: 0..3 (width 4), Expanded y: 0..3 (height 4).
    # Area = 4 * 4 = 16.
    # Why did I think 3*3?
    # Coordinates: 0, 1, 2, 3. Count is 4.
    # Width = w1+1 = 3? No.
    # Ship x range: [1, w1]. Size w1.
    # Neighbors: x-1 and x+1.
    # Min x = 1-1 = 0. Max x = w1+1.
    # Number of integers from 0 to w1+1 inclusive is (w1+1) - 0 + 1 = w1 + 2.
    # Ah! The dimension calculation was wrong.
    # Size of range [A, B] inclusive is B - A + 1.
    # Expanded X range: [0, w1+1]. Size = w1 + 2.
    # Expanded Y range: [0, h1+h2+1]. Size = h1 + h2 + 2.
    #
    # Correct Calculation:
    # Total Box Area = (w1 + 2) * (h1 + h2 + 2).
    # Ship Area = w1*h1 + w2*h2.
    # Unmarked Area inside box (the "hole" in the L-shape corner):
    # x in [w2+1, w1], y in [h1+2, h1+h2+1].
    # Width = w1 - w2.
    # Height = (h1+h2+1) - (h1+2) + 1 = h2.
    # Unmarked = (w1 - w2) * h2.
    #
    # Final Formula:
    # Ans = (w1 + 2) * (h1 + h2 + 2) - (w1*h1 + w2*h2) - (w1 - w2)*h2
    #
    # Let's re-test Example 1: w1=2, h1=1, w2=2, h2=1.
    # Box = 4 * 4 = 16.
    # Ship = 2*1 + 2*1 = 4.
    # Unmarked = (2-2)*1 = 0.
    # Ans = 16 - 4 = 12. Matches.
    #
    # Example 2: w1=2, h1=2, w2=1, h2=2.
    # Box = (2+2) * (2+2+2) = 4 * 6 = 24.
    # Ship = 2*2 + 1*2 = 4 + 2 = 6.
    # Unmarked = (2-1) * 2 = 2.
    # Ans = 24 - 6 - 2 = 16. Matches.
    
    ans = (w1 + 2) * (h1 + h2 + 2) - (w1 * h1 + w2 * h2) - (w1 - w2) * h2
    print(ans)

if __name__ == '__main__':
    solve()