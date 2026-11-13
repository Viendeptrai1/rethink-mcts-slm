from collections import deque

def minPath(grid, k):
    n = len(grid)
    # Convert grid to 1D array for easier indexing if needed, but 2D is fine too.
    # We need to find the lexicographically smallest path of length k.
    # Since k can be up to N*N (in worst case) and N can be reasonably large, 
    # but note: the problem says values are 1 to N*N exactly once.
    # However, k is given and we must take exactly k cells.
    # Important: k might be large, so BFS might be too slow if we explore all paths.
    # But note: we are looking for the lexicographically smallest path.
    # The first element of the path should be the smallest possible value in the grid.
    # Then the second element should be the smallest possible value reachable from the first, and so on.
    # However, caution: taking the smallest current value might lead to a dead end or force a large value later.
    # But the problem asks for the lexicographically smallest path. Lexicographic comparison is decided at the first differing index.
    # Therefore, we must minimize the first element, then the second, etc.
    # So we can do a BFS that expands level by level, but only keeping the best path to each state? 
    # However, the state is just the current cell. But we also need to remember the path? 
    # Actually, for lexicographic order, at each step we want to choose the smallest next value that can lead to a complete path of length k.
    # But note: we don't care about the entire future path for lexicographic order until we hit a difference. 
    # However, if we have two paths that are identical up to step i, and at step i+1 we have choices, 
    # we pick the smallest value at step i+1. But what if picking the smallest at step i+1 leads to no path of length k? 
    # Then we cannot pick it. So we must ensure that from the chosen cell at step i, there exists a path of length k-i-1.
    # But note: the grid is connected (it's a grid graph) and we can revisit cells. So as long as k-i-1 >= 0, we can always stay in place? 
    # But we cannot stay in place; we must move to a neighbor. However, the grid is connected and has cycles (since N>=2), 
    # so from any cell, we can make arbitrarily long paths. Therefore, if k is not too large, we don't have the "dead end" problem.
    # Actually, since we can revisit cells, and the grid is connected, we can always extend the path as long as k is positive.
    # Therefore, the only constraint is: at each step, we can pick the smallest neighbor value that is available.
    # But wait: what if the smallest neighbor value is the same as the current? That's allowed (revisiting).
    # So the algorithm is:
    #   Start at the cell with the minimum value in the entire grid. (Because the first element of the path must be minimized)
    #   Then, for the next k-1 steps, from the current cell, move to the neighbor with the smallest value.
    #   Why? Because if we have a choice between two neighbors with values v1 and v2 (v1 < v2), then any path starting with ... v1 ... 
    #   is lexicographically smaller than any path starting with ... v2 ... at that position, regardless of what comes after.
    #   And since we can always extend the path (because the grid is connected and we can revisit), there is no risk of getting stuck.
    # Therefore, the greedy strategy works.

    # Step 1: Find the starting cell (the one with the minimum value in the grid)
    min_val = float('inf')
    start_r, start_c = -1, -1
    for r in range(n):
        for c in range(n):
            if grid[r][c] < min_val:
                min_val = grid[r][c]
                start_r, start_c = r, c

    # Step 2: Build the path of length k
    path = [min_val]
    curr_r, curr_c = start_r, start_c

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for _ in range(k - 1):
        best_next_val = float('inf')
        best_next_r, best_next_c = -1, -1
        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < n and 0 <= nc < n:
                val = grid[nr][nc]
                if val < best_next_val:
                    best_next_val = val
                    best_next_r, best_next_c = nr, nc
        # Move to the best next cell
        curr_r, curr_c = best_next_r, best_next_c
        path.append(best_next_val)

    return path