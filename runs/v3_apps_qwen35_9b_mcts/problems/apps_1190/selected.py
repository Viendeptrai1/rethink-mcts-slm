import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    w1 = int(input_data[0])
    h1 = int(input_data[1])
    w2 = int(input_data[2])
    h2 = int(input_data[3])
    
    # The shape consists of two rectangles:
    # Bottom: width w1, height h1
    # Top: width w2, height h2, aligned left on top of the bottom one.
    # Since w1 >= w2, the top rectangle is narrower or equal width.
    
    # The number of marked cells (neighbors by side or corner) can be calculated by:
    # 1. Counting the perimeter cells (side neighbors).
    # 2. Counting the corner cells (diagonal neighbors).
    
    # Let's break down the perimeter:
    # Bottom rectangle (w1 x h1):
    #   - Bottom edge: w1 cells
    #   - Left edge: h1 cells (excluding bottom corner already counted? No, let's do full perimeter then adjust)
    #   - Right edge: h1 cells
    #   - Top edge: w1 cells
    #   Total perimeter cells for a single rect = 2*(w1+h1). But corners are shared.
    #   Actually, let's count unique side neighbors.
    
    # Alternative approach:
    # The set of marked cells is the set of all cells (x, y) such that:
    # dist((x,y), ship) <= 1 (Chebyshev distance) AND (x,y) is not in ship.
    # This is equivalent to: Area of the "dilated" shape minus Area of the ship.
    # Dilating a shape by 1 in Chebyshev distance adds a border of width 1 around it.
    # For a rectangle of size WxH, the dilated area is (W+2)*(H+2).
    # The number of marked cells for a single rectangle is (W+2)*(H+2) - W*H = 2W + 2H + 4.
    
    # However, we have two connected rectangles. The union of their dilated sets minus the union of the rectangles themselves.
    # Let S1 be the set of cells in rect1, S2 in rect2.
    # Marked = |D(S1 U S2)| - |S1 U S2|
    # Where D(S) is the set of cells within Chebyshev distance 1 of S.
    # D(S1 U S2) = D(S1) U D(S2).
    # So Marked = |D(S1) U D(S2)| - |S1 U S2|
    # = |D(S1)| + |D(S2)| - |D(S1) n D(S2)| - (|S1| + |S2| - |S1 n S2|)
    # = (|D(S1)| - |S1|) + (|D(S2)| - |S2|) + |S1 n S2| - |D(S1) n D(S2)|
    
    # |D(S1)| - |S1| = 2*w1 + 2*h1 + 4
    # |D(S2)| - |S2| = 2*w2 + 2*h2 + 4
    # |S1 n S2| = 0 (they are adjacent, not overlapping)
    # So we need to subtract |D(S1) n D(S2)|.
    
    # S1: x in [1, w1], y in [1, h1]
    # S2: x in [1, w2], y in [h1+1, h1+h2]
    # D(S1): x in [0, w1+1], y in [0, h1+1]
    # D(S2): x in [0, w2+1], y in [h1, h1+h2+1]
    
    # Intersection D(S1) n D(S2):
    # x range: [0, w1+1] n [0, w2+1] = [0, w2+1] (since w1 >= w2)
    # y range: [0, h1+1] n [h1, h1+h2+1] = [h1, h1+1]
    # So the intersection is a rectangle of width (w2+1) - 0 + 1 = w2+2?
    # Wait, integer coordinates.
    # x from 0 to w2+1 inclusive -> count = w2+2
    # y from h1 to h1+1 inclusive -> count = 2
    # So |D(S1) n D(S2)| = (w2 + 2) * 2 = 2*w2 + 4.
    
    # Let's re-verify the formula:
    # Marked = (2*w1 + 2*h1 + 4) + (2*w2 + 2*h2 + 4) - (2*w2 + 4)
    # Marked = 2*w1 + 2*h1 + 2*w2 + 2*h2 + 8 - 2*w2 - 4
    # Marked = 2*w1 + 2*h1 + 2*h2 + 4
    
    # Let's test with Example 1: w1=2, h1=1, w2=2, h2=1
    # Formula: 2*2 + 2*1 + 2*1 + 4 = 4 + 2 + 2 + 4 = 12. Correct.
    
    # Example 2: w1=2, h1=2, w2=1, h2=2
    # Formula: 2*2 + 2*2 + 2*2 + 4 = 4 + 4 + 4 + 4 = 16. Correct.
    
    # Is there any edge case where w1 > w2 affects the intersection?
    # The intersection x-range is determined by the smaller width w2.
    # The intersection y-range is always the single line between the two rects plus the boundary cells?
    # D(S1) y-range: 0 to h1+1.
    # D(S2) y-range: h1 to h1+h2+1.
    # Overlap: h1, h1+1. Length 2.
    # This holds regardless of w1 vs w2 as long as they are adjacent vertically.
    # The x-overlap is 0 to min(w1, w2)+1. Since w1 >= w2, it is 0 to w2+1. Length w2+2.
    # So the logic holds.
    
    ans = 2 * w1 + 2 * h1 + 2 * h2 + 4
    print(ans)

if __name__ == '__main__':
    solve()