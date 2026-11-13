import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    board = []
    for _ in range(n):
        board.append(list(next(iterator)))

    # Directions for the 5 cells of the piece: center and 4 neighbors
    # We will try to place the center of a piece at (r, c)
    # The cells covered would be (r, c), (r-1, c), (r+1, c), (r, c-1), (r, c+1)
    offsets = [
        (0, 0),
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    # We need to fill all '.' cells.
    # Since n is small (up to 50), we can use a recursive backtracking approach with memoization or just simple backtracking with pruning.
    # However, simple backtracking on a 50x50 grid might be too slow if not ordered well.
    # A common strategy for tiling problems is to find the first empty cell and try to cover it.
    # The first empty cell must be covered by some piece.
    # For a cell (r, c) to be the "center" of a piece, all 5 cells must be within bounds and currently free.
    # But wait, the piece shape is fixed: one center and 4 orthogonal neighbors.
    # If we encounter the first free cell (r, c), it MUST be covered.
    # Which position within the piece does (r, c) correspond to?
    # It could be the center, or one of the 4 arms.
    # However, if we process cells in row-major order, when we are at (r, c) and it is free:
    # 1. It could be the center of a new piece. Then we must place a piece with center at (r, c). This requires (r-1, c), (r+1, c), (r, c-1), (r, c+1) to be free and valid.
    #    But note: if (r, c) is the center, then (r, c-1) must be covered by this piece. But (r, c-1) was already processed (since we go row by row, left to right). If (r, c-1) was free and we didn't cover it yet, then (r, c) cannot be the center because (r, c-1) would have been handled already? 
    #    Actually, if (r, c-1) was free, we would have tried to cover it. If we covered it as an arm of a piece centered at (r, c-1) or (r, c-1)'s neighbors, then it's done.
    #    If (r, c-1) is free, and we are now at (r, c), and we decide (r, c) is the center, then (r, c-1) must be covered by this piece. But (r, c-1) < (r, c) in order. So (r, c-1) would have been left free? That contradicts "first free cell".
    #    Therefore, if (r, c) is the first free cell, it CANNOT be the center of a piece because that would require (r, c-1) to be covered, but (r, c-1) is either occupied or already covered. If (r, c-1) is occupied, then placing a piece centered at (r, c) would cover (r, c-1) which is invalid. If (r, c-1) is free, then (r, c) is not the first free cell.
    #    So, if (r, c) is the first free cell, it must be an ARM of a piece.
    # Which arm?
    # The piece has arms at (r-1, c), (r+1, c), (r, c-1), (r, c+1) relative to center.
    # Since (r, c) is the first free cell in row-major order:
    # - (r, c-1) must be occupied or covered. If it's covered, it's not free. If it's occupied, we can't place a piece that covers it. So (r, c) cannot be the right arm (c+1) of a center at (r, c-1) because that would cover (r, c-1) which is fine, but wait...
    # Let's refine:
    # We iterate r from 0 to n-1, c from 0 to n-1.
    # If board[r][c] == '#', continue.
    # If board[r][c] == '.', we MUST cover it now.
    # Try all possible roles for (r, c) in a piece:
    # 1. (r, c) is the center. Then we need neighbors (r-1, c), (r+1, c), (r, c-1), (r, c+1) to be free.
    #    But as argued, if (r, c) is the first free cell, (r, c-1) cannot be free. So if (r, c-1) is free, this case is impossible? 
    #    Actually, the standard greedy strategy for this specific shape (plus shape) works like this:
    #    The first free cell (r, c) MUST be covered. 
    #    Can it be the center? Only if all neighbors are free. But if (r, c-1) is free, then (r, c) is not the first free cell. So if (r, c) is the first free cell, (r, c-1) is not free. Thus, (r, c) cannot be the center because the left neighbor is not free.
    #    Can it be the right arm of a center at (r, c-1)? Then center is (r, c-1). Neighbors needed: (r-1, c-1), (r+1, c-1), (r, c-2), (r, c).
    #    But (r, c-1) would be the center. Was (r, c-1) free? If (r, c-1) was free, we would have processed it before (r, c). So (r, c-1) must have been covered already. Contradiction.
    #    Therefore, the first free cell cannot be covered by a piece whose center is to its left.
    #    Similarly, can it be the bottom arm of a center at (r-1, c)? Center (r-1, c). Then (r-1, c) would have been processed before (r, c). So (r-1, c) is covered. Contradiction.
    #    Can it be the top arm of a center at (r+1, c)? Center (r+1, c). This is a future cell. This is possible. The piece is centered at (r+1, c) and extends up to (r, c).
    #    Can it be the left arm of a center at (r, c+1)? Center (r, c+1). Future cell. Possible.
    #    So, the first free cell (r, c) can only be covered by:
    #      a) A piece centered at (r+1, c) where (r, c) is the top arm.
    #      b) A piece centered at (r, c+1) where (r, c) is the left arm.
    #      c) A piece centered at (r, c) where (r, c) is the center? We established (r, c-1) must be free for this, which is impossible if (r, c) is the first free cell. UNLESS (r, c-1) is out of bounds (column -1).
    #      d) A piece centered at (r-1, c)? No, center processed.
    #      e) A piece centered at (r+1, c) is valid.
    #      f) A piece centered at (r, c+1) is valid.
    #      g) What if (r, c) is the bottom arm? Center at (r-1, c). Center processed. Invalid.
    #      h) What if (r, c) is the right arm? Center at (r, c-1). Center processed. Invalid.
    #    So only possibilities for the FIRST free cell (r, c):
    #      1. Center at (r+1, c) [Top arm]
    #      2. Center at (r, c+1) [Left arm]
    #      3. Center at (r, c) [Center itself] -> Only if (r, c-1) is out of bounds (i.e., c==0).
    #    Wait, let's re-evaluate "Center at (r, c)".
    #    If c == 0, then (r, c-1) is out of bounds. The condition "all neighbors free" is not applicable to out of bounds cells in the sense that we can't place the piece. The piece must fit entirely in the board. So if c==0, we cannot place a piece centered at (r, c) because it requires (r, c-1).
    #    So if c==0, (r, c) cannot be a center.
    #    If c > 0, (r, c-1) exists. If (r, c) is the first free cell, (r, c-1) is either '#' or already covered. If it's '#', we can't place a piece centered at (r, c). If it's covered, it's not '.' so we can't place.
    #    So (r, c) can NEVER be the center if it is the first free cell.
    #    Therefore, the first free cell MUST be an arm of a piece centered at a future cell.
    #    Possibilities:
    #      - Center at (r+1, c): requires (r+1, c), (r, c), (r+2, c), (r+1, c-1), (r+1, c+1) to be free.
    #      - Center at (r, c+1): requires (r, c+1), (r-1, c+1), (r+1, c+1), (r, c), (r, c+2) to be free.
    #    Are there any other cases?
    #      - Center at (r-1, c): Top arm is (r-2, c), Bottom arm is (r, c). But center (r-1, c) was processed earlier. So it's already covered. Can't be center now.
    #    So exactly two possibilities for the first free cell (r, c):
    #      Option 1: Place piece centered at (r+1, c).
    #      Option 2: Place piece centered at (r, c+1).
    #    We try both. If one leads to a solution, return YES. If both fail, return NO.
    #    Base case: if no free cells left, return YES.
    
    # Mark free cells as a set or modify the board.
    # Since we need to backtrack, modifying the board and reverting is efficient.
    
    def backtrack():
        # Find first free cell
        for r in range(n):
            for c in range(n):
                if board[r][c] == '.':
                    return try_fill(r, c)
        return True

    def try_fill(r, c):
        # Try Option 1: Center at (r+1, c)
        # Check bounds for center: r+1 < n
        # Check all 5 cells are free
        r1, c1 = r + 1, c
        if r1 < n:
            if (is_valid_center(r1, c1)):
                place_piece(r1, c1)
                if backtrack():
                    undo_piece(r1, c1)
                    return True
                undo_piece(r1, c1)

        # Try Option 2: Center at (r, c+1)
        # Check bounds for center: c+1 < n
        r2, c2 = r, c + 1
        if c2 < n:
            if (is_valid_center(r2, c2)):
                place_piece(r2, c2)
                if backtrack():
                    undo_piece(r2, c2)
                    return True
                undo_piece(r2, c2)
        
        return False

    def is_valid_center(cr, cc):
        # Check bounds for all 5 cells
        cells = [(cr, cc), (cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)]
        for r, c in cells:
            if not (0 <= r < n and 0 <= c < n):
                return False
            if board[r][c] != '.':
                return False
        return True

    def place_piece(cr, cc):
        cells = [(cr, cc), (cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)]
        for r, c in cells:
            board[r][c] = '#'

    def undo_piece(cr, cc):
        cells = [(cr, cc), (cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)]
        for r, c in cells:
            board[r][c] = '.'

    if backtrack():
        print("YES")
    else:
        print("NO")

if __name__ == '__main__':
    solve()