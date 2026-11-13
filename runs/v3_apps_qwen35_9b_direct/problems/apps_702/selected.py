import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    grid = []
    idx = 1
    for _ in range(n):
        grid.append(list(input_data[idx]))
        idx += 1
    
    # Directions for the 4 neighbors of a center cell
    # (row_offset, col_offset)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # We will try to greedily place pieces. 
    # Strategy: Iterate through every cell. If a cell is free ('.'), it MUST be part of some piece.
    # Since pieces are 5-connected (center + 4 neighbors), a free cell can be:
    # 1. The center of a piece.
    # 2. A neighbor of a center.
    #
    # To make the problem deterministic and solvable via simple backtracking/greedy:
    # We can enforce an ordering. For example, we scan from top-left to bottom-right.
    # When we encounter a free cell, we try to cover it.
    # However, simply trying to make it a center might not work if it's better to be a neighbor.
    #
    # Better approach: Backtracking with pruning.
    # Find the first free cell (in row-major order).
    # Try all possible ways this cell can be covered by a piece.
    # A piece covering this cell can have this cell as:
    #   - The center. Then the 4 neighbors must be free and within bounds.
    #   - A neighbor. Then the center must be one of the 4 adjacent cells, and that center's other 3 neighbors must be free.
    #
    # Actually, since the piece shape is fixed (center + 4 neighbors), any placement is defined by its center.
    # So, if we decide to place a piece with center at (r, c), it covers (r,c) and its 4 neighbors.
    #
    # Revised Greedy/Backtracking Strategy:
    # 1. Find the first free cell (r, c) in row-major order.
    # 2. This cell MUST be covered. It can be covered by a piece centered at:
    #    a) (r, c) itself.
    #    b) (r-1, c) [if r>0]
    #    c) (r+1, c) [if r<n-1]
    #    d) (r, c-1) [if c>0]
    #    e) (r, c+1) [if c<n-1]
    # 3. For each potential center, check if placing a piece there is valid:
    #    - The center must be free.
    #    - All 4 neighbors of the center must be within bounds and free.
    #    - Note: If the current cell (r,c) is a neighbor of the center, the center itself must be free.
    # 4. If valid, place the piece (mark cells as occupied), recurse.
    # 5. If recursion returns True, we are done.
    # 6. If no placement works for the current free cell, backtrack and return False.
    #
    # Optimization: Since we process in row-major order, the "first free cell" is always the top-leftmost remaining free cell.
    # This reduces the search space significantly because we don't have choices about WHICH free cell to cover next; 
    # we are forced to cover the first one. The only choices are HOW to cover it (which of the 5 relative positions is the center).
    
    def find_first_free():
        for r in range(n):
            for c in range(n):
                if grid[r][c] == '.':
                    return r, c
        return None

    def can_place_center(r, c):
        # Check if center (r,c) is valid
        if r < 0 or r >= n or c < 0 or c >= n:
            return False
        if grid[r][c] != '.':
            return False
        
        # Check all 4 neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= n or nc < 0 or nc >= n:
                return False
            if grid[nr][nc] != '.':
                return False
        return True

    def place_piece(r, c):
        grid[r][c] = '#'
        for dr, dc in directions:
            grid[r+dr][c+dc] = '#'

    def remove_piece(r, c):
        grid[r][c] = '.'
        for dr, dc in directions:
            grid[r+dr][c+dc] = '.'

    def backtrack():
        pos = find_first_free()
        if pos is None:
            return True  # All cells covered
        
        r, c = pos
        
        # Try making (r,c) the center
        if can_place_center(r, c):
            place_piece(r, c)
            if backtrack():
                return True
            remove_piece(r, c)
        
        # Try making (r,c) a neighbor. The center would be one of the 4 adjacent cells.
        # Potential centers: (r-1, c), (r+1, c), (r, c-1), (r, c+1)
        potential_centers = [
            (r-1, c),
            (r+1, c),
            (r, c-1),
            (r, c+1)
        ]
        
        for cr, cc in potential_centers:
            if can_place_center(cr, cc):
                place_piece(cr, cc)
                if backtrack():
                    return True
                remove_piece(cr, cc)
        
        return False

    if backtrack():
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()