import sys

# Increase recursion depth for deep DFS
sys.setrecursionlimit(20000)

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    if m == 0:
        print(0)
        return

    rects = []
    xs = set()
    ys = set()
    
    for _ in range(m):
        x1 = int(next(iterator))
        y1 = int(next(iterator))
        x2 = int(next(iterator))
        y2 = int(next(iterator))
        rects.append((x1, y1, x2, y2))
        xs.add(x1)
        xs.add(x2 + 1)
        ys.add(y1)
        ys.add(y2 + 1)
    
    xs = sorted(list(xs))
    ys = sorted(list(ys))
    
    x_map = {x: i for i, x in enumerate(xs)}
    y_map = {y: i for i, y in enumerate(ys)}
    
    num_x = len(xs)
    num_y = len(ys)
    
    # Create a grid of booleans representing if a cell is black
    # Grid dimensions: num_x x num_y
    # We will use a 2D array where grid[i][j] is True if the elementary rectangle
    # defined by xs[i]..xs[i+1] and ys[j]..ys[j+1] contains any black cell.
    
    grid = [[False] * num_y for _ in range(num_x)]
    
    for (x1, y1, x2, y2) in rects:
        xi1 = x_map[x1]
        xi2 = x_map[x2 + 1]
        yi1 = y_map[y1]
        yi2 = y_map[y2 + 1]
        
        for i in range(xi1, xi2):
            for j in range(yi1, yi2):
                grid[i][j] = True
    
    # Precompute prefix sums to quickly check if a sub-rectangle has any black cells
    # pref[i][j] = sum of grid[0..i-1][0..j-1]
    pref = [[0] * (num_y + 1) for _ in range(num_x + 1)]
    for i in range(num_x):
        for j in range(num_y):
            pref[i+1][j+1] = pref[i][j+1] + pref[i+1][j] - pref[i][j] + (1 if grid[i][j] else 0)
    
    def has_black(x1_idx, y1_idx, x2_idx, y2_idx):
        # Check if rectangle [x1_idx, x2_idx) x [y1_idx, y2_idx) has any black cell
        return pref[x2_idx][y2_idx] - pref[x1_idx][y2_idx] - pref[x2_idx][y1_idx] + pref[x1_idx][y1_idx] > 0

    # Memoization cache
    memo = {}

    def dp(x1_idx, y1_idx, x2_idx, y2_idx):
        # Returns min cost to clear the rectangle defined by indices
        # Coordinates in original space:
        # x range: xs[x1_idx] to xs[x2_idx]
        # y range: ys[y1_idx] to ys[y2_idx]
        
        state = (x1_idx, y1_idx, x2_idx, y2_idx)
        if state in memo:
            return memo[state]
        
        # Calculate actual width and height in original coordinates
        w = xs[x2_idx] - xs[x1_idx]
        h = ys[y2_idx] - ys[y1_idx]
        
        # If no black cells in this region, cost is 0
        if not has_black(x1_idx, y1_idx, x2_idx, y2_idx):
            return 0
        
        # Option 1: Clear the whole rectangle with one operation
        cost = min(h, w)
        
        # Option 2: Split horizontally
        # Try every possible split line between x1_idx and x2_idx
        # Split at k: left part [x1_idx, k), right part [k, x2_idx)
        # We only need to check splits where both parts might contain black cells
        # to potentially reduce cost.
        
        # Optimization: Only consider splits that actually divide the black area
        # But since m is small and grid is compressed, we can iterate.
        # However, iterating all k is O(num_x). Total states O(num_x^2 * num_y^2).
        # num_x, num_y <= 2*m + 2 <= 102. 102^4 is ~100 million, might be tight.
        # We need to be careful. But note: we only care about splits that separate black regions.
        # Actually, the standard approach for this problem (Codeforces 1196F2 / similar) 
        # is to try all splits. Given m <= 50, num_x <= 102.
        # Let's implement with pruning: if cost is already 0, stop.
        # Also, we can stop if we found a cost of 1 (minimum possible non-zero).
        
        best = cost
        
        # Horizontal split: split x-range
        for k in range(x1_idx + 1, x2_idx):
            # Left part
            c1 = dp(x1_idx, y1_idx, k, y2_idx)
            # Right part
            c2 = dp(k, y1_idx, x2_idx, y2_idx)
            if c1 + c2 < best:
                best = c1 + c2
                if best == 0:
                    break
        
        if best == 0:
            memo[state] = 0
            return 0
            
        # Vertical split: split y-range
        for k in range(y1_idx + 1, y2_idx):
            # Top part
            c1 = dp(x1_idx, y1_idx, x2_idx, k)
            # Bottom part
            c2 = dp(x1_idx, k, x2_idx, y2_idx)
            if c1 + c2 < best:
                best = c1 + c2
                if best == 0:
                    break
        
        memo[state] = best
        return best

    # Initial call covering the entire bounding box of the black cells
    # Find min/max x and y from rects
    min_x = min(r[0] for r in rects)
    max_x = max(r[2] for r in rects)
    min_y = min(r[1] for r in rects)
    max_y = max(r[3] for r in rects)
    
    idx_x1 = x_map[min_x]
    idx_x2 = x_map[max_x + 1]
    idx_y1 = y_map[min_y]
    idx_y2 = y_map[max_y + 1]
    
    print(dp(idx_x1, idx_y1, idx_x2, idx_y2))

if __name__ == '__main__':
    solve()