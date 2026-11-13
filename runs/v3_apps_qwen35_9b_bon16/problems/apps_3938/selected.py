import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return 0

    if m == 0:
        print(0)
        return

    rects = []
    for _ in range(m):
        x1 = int(next(iterator))
        y1 = int(next(iterator))
        x2 = int(next(iterator))
        y2 = int(next(iterator))
        rects.append((x1, y1, x2, y2))

    # Collect all unique x and y coordinates to compress the grid
    xs = set()
    ys = set()
    xs.add(1)
    xs.add(n + 1)
    ys.add(1)
    ys.add(n + 1)
    
    for x1, y1, x2, y2 in rects:
        xs.add(x1)
        xs.add(x2 + 1)
        ys.add(y1)
        ys.add(y2 + 1)
    
    xs = sorted(list(xs))
    ys = sorted(list(ys))
    
    # Create coordinate maps
    x_map = {val: i for i, val in enumerate(xs)}
    y_map = {val: i for i, val in enumerate(ys)}
    
    # Build the compressed grid (0 for white, 1 for black)
    # Grid dimensions: (len(xs)-1) x (len(ys)-1)
    num_x = len(xs) - 1
    num_y = len(ys) - 1
    grid = [[0] * num_x for _ in range(num_y)]
    
    for x1, y1, x2, y2 in rects:
        xi1 = x_map[x1]
        yi1 = y_map[y1]
        xi2 = x_map[x2 + 1] - 1
        yi2 = y_map[y2 + 1] - 1
        
        for r in range(yi1, yi2 + 1):
            for c in range(xi1, xi2 + 1):
                grid[r][c] = 1

    # Function to compute cost to clear a rectangular region in the compressed grid
    # Using dynamic programming or iterative approach for small grids
    # Since num_x, num_y <= 2*m + 2 ~ 102, we can use a recursive DP with memoization
    # or a simple iterative approach for sub-rectangles.
    
    # We need a function to get the bounding box of black cells in a range
    # and compute the min cost to clear that specific rectangle in the grid.
    
    # Let's define a function min_cost_rect(r1, r2, c1, c2) which returns the min cost
    # to clear all black cells within the compressed rectangle [r1, r2] x [c1, c2].
    # Note: The cost of an operation on a rectangle of height h and width w in the ORIGINAL grid
    # is min(h_orig, w_orig).
    # In our compressed grid, a single cell corresponds to a block of size (xs[i+1]-xs[i]) x (ys[j+1]-ys[j]).
    # However, the problem allows us to pick ANY rectangle in the original grid.
    # When we operate on a union of compressed cells, the resulting rectangle in the original grid
    # will have height = sum of heights of rows involved and width = sum of widths of cols involved.
    # But wait, the standard solution for this problem (Codeforces 1251E? No, this is likely "Painting the Grid" variant)
    # actually simplifies because we can always choose to paint row by row or column by column if it's optimal?
    # No, the cost is min(h, w).
    
    # Actually, the key insight for this specific problem (from similar CP problems) is:
    # We can compute the min cost for a rectangle defined by compressed coordinates.
    # However, since the cost depends on the SUM of intervals, we cannot simply sum costs of sub-rectangles.
    # BUT, notice that if we decide to clear a set of black cells, we can always cover them with a single
    # operation if they form a rectangle? No, they might not.
    # The strategy usually involves trying to split the rectangle either horizontally or vertically.
    # But the cost function min(h, w) makes standard split DP tricky because the cost of the split part
    # depends on the full dimensions of the sub-rectangle we CHOOSE to paint, which might be larger than the black part.
    
    # Let's reconsider the problem constraints and properties.
    # m <= 50 -> compressed grid is small (~100x100).
    # We need to find min cost to clear ALL black cells.
    # This is equivalent to finding a set of rectangles that cover all black cells with min sum of min(h, w).
    # Since we can pick ANY rectangle, we should pick the minimal bounding box of the black cells we are covering?
    # Yes, expanding the rectangle beyond the black cells doesn't help (cost increases or stays same, coverage same).
    # So for any subset of black cells we cover in one operation, the cost is min(H, W) where H, W are the span of that subset.
    
    # This looks like a variation of the "minimum cost to cover points" but with rectangles and min(h,w).
    # Given the small grid size, we can use recursion with memoization on the bounding box of black cells.
    # State: (r_min, r_max, c_min, c_max) representing the bounding box of the black cells we need to clear.
    # But simply splitting might not be enough if the optimal move covers a larger area than the current bounding box?
    # No, we only care about clearing black cells. Any white cell we cover is "free" in terms of necessity,
    # but it contributes to h and w. So we should always choose the rectangle exactly fitting the black cells
    # we intend to clear in one go?
    # Not necessarily. Sometimes covering a slightly larger area allows us to clear multiple disjoint components
    # cheaper than two separate operations?
    # Example: Two separate 1x1 blocks at (0,0) and (0,2). 
    # Option 1: Two ops of 1x1 -> cost 1+1=2.
    # Option 2: One op of 1x3 (covering (0,0) to (0,2)) -> cost min(1,3)=1.
    # So yes, we might cover extra white space.
    
    # However, note that if we cover a rectangle, we pay min(H, W).
    # If we have multiple disjoint components, merging them into one rectangle might be beneficial if min(H, W) < sum(min(h_i, w_i)).
    # This suggests we need to consider splitting the current bounding box into two parts (horizontal or vertical split)
    # and then solve recursively.
    # Base case: If no black cells in the region, cost 0.
    # Recursive step:
    #   Option A: Clear the entire bounding box in one go. Cost = min(total_h, total_w).
    #   Option B: Split the bounding box horizontally or vertically at every possible line, sum the costs of the two parts.
    #   Take the minimum.
    
    # Wait, is "Clear the entire bounding box in one go" always an option?
    # Yes, because we can just select the rectangle defined by the bounding box of the current set of black cells.
    # This clears all black cells inside it. Any remaining black cells outside this box must be handled by other ops.
    # But our DP state is defined by the bounding box of the BLACK cells we still need to clear.
    # If we choose to clear the whole bounding box, we are done with this set (cost = min(h, w)).
    # If we split, we pay cost(split1) + cost(split2).
    # Is it possible that the optimal solution involves a rectangle that is NOT the bounding box of the remaining black cells?
    # Suppose we have black cells at (0,0) and (10, 10). Bounding box is 11x11. Cost min(11,11)=11.
    # Split: (0,0) -> cost 1, (10,10) -> cost 1. Total 2.
    # Suppose we have black cells at (0,0), (0,1), (1,0), (1,1). Bounding box 2x2. Cost 2.
    # Split: (0,0)-(0,1) cost 1, (1,0)-(1,1) cost 1 -> total 2.
    # Split: (0,0)-(1,0) cost 1, (0,1)-(1,1) cost 1 -> total 2.
    # It seems the split strategy works.
    # What if we have a "C" shape?
    # (0,0), (0,1), (0,2), (1,0), (2,0). Bounding box 3x3. Cost 3.
    # Split vertical at x=1: Left (col 0-1) has (0,0),(0,1),(1,0),(2,0)? No.
    # Let's formalize the DP.
    
    # We first find the global bounding box of all black cells.
    # Then we define a function f(r1, r2, c1, c2) which is the min cost to clear all black cells
    # contained within the compressed rectangle [r1, r2] x [c1, c2].
    # Note: The rectangle might contain white cells.
    # The cost to clear THIS specific rectangle (meaning, apply one operation covering exactly this area)
    # is min(height_in_original, width_in_original).
    # But we might choose to split this rectangle into two sub-rectangles and clear them separately.
    
    # Precompute height and width of compressed cells to quickly calculate original dimensions.
    row_h = [xs[i+1] - xs[i] for i in range(num_x)]
    row_w = [ys[i+1] - ys[i] for i in range(num_y)] # Actually row_w should be associated with columns
    
    col_w = [ys[i+1] - ys[i] for i in range(num_y)]
    
    # Precompute if a compressed cell (r, c) is black
    is_black = grid # grid[r][c]
    
    # Check if there are any black cells in the range [r1, r2] x [c1, c2]
    def has_black(r1, r2, c1, c2):
        if r1 > r2 or c1 > c2:
            return False
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if is_black[r][c]:
                    return True
        return False

    # Calculate original dimensions of the compressed rectangle
    def get_dims(r1, r2, c1, c2):
        h = sum(row_h[r] for r in range(r1, r2 + 1))
        w = sum(col_w[c] for c in range(c1, c2 + 1))
        return h, w

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(r1, r2, c1, c2):
        # Check if there are black cells
        if not has_black(r1, r2, c1, c2):
            return 0
        
        # Option 1: Clear the whole rectangle with one operation
        h, w = get_dims(r1, r2, c1, c2)
        cost_one = min(h, w)
        
        # Option 2: Split horizontally
        best_split = float('inf')
        # Try all horizontal splits between r and r+1
        for i in range(r1, r2):
            left_cost = dp(r1, i, c1, c2)
            right_cost = dp(i + 1, r2, c1, c2)
            best_split = min(best_split, left_cost + right_cost)
        
        # Option 3: Split vertically
        for i in range(c1, c2):
            left_cost = dp(r1, r2, c1, i)
            right_cost = dp(r1, r2, i + 1, c2)
            best_split = min(best_split, left_cost + right_cost)
        
        return min(cost_one, best_split)

    # Find global bounding box
    min_r, max_r = num_y, -1
    min_c, max_c = num_x, -1
    
    for r in range(num_y):
        for c in range(num_x):
            if is_black[r][c]:
                if r < min_r: min_r = r
                if r > max_r: max_r = r
                if c < min_c: min_c = c
                if c > max_c: max_c = c
    
    if min_r > max_r or min_c > max_c:
        print(0)
        return

    result = dp(min_r, max_r, min_c, max_c)
    print(result)

solve()