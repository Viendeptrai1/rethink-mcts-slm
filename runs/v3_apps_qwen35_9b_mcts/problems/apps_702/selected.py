import sys

# Increase recursion depth just in case, though for n=50 it should be fine.
sys.setrecursionlimit(20000)

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    n = int(data[0])
    board = []
    idx = 1
    for _ in range(n):
        board.append(list(data[idx]))
        idx += 1

    # Find the first free cell in row-major order
    def find_first_free():
        for r in range(n):
            for c in range(n):
                if board[r][c] == '.':
                    return (r, c)
        return None

    # Check if a piece can be placed with center at (cr, cc)
    # The piece covers: (cr, cc), (cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)
    def can_place(cr, cc):
        # Check bounds for all 5 cells
        if not (0 <= cr-1 < n and 0 <= cr+1 < n and 0 <= cc-1 < n and 0 <= cc+1 < n):
            return False
        
        # Check if all 5 cells are free
        cells = [
            (cr, cc),
            (cr-1, cc),
            (cr+1, cc),
            (cr, cc-1),
            (cr, cc+1)
        ]
        for r, c in cells:
            if board[r][c] != '.':
                return False
        return True

    # Place the piece
    def place_piece(cr, cc):
        cells = [
            (cr, cc),
            (cr-1, cc),
            (cr+1, cc),
            (cr, cc-1),
            (cr, cc+1)
        ]
        for r, c in cells:
            board[r][c] = '#'

    # Remove the piece
    def remove_piece(cr, cc):
        cells = [
            (cr, cc),
            (cr-1, cc),
            (cr+1, cc),
            (cr, cc-1),
            (cr, cc+1)
        ]
        for r, c in cells:
            board[r][c] = '.'

    def backtrack():
        pos = find_first_free()
        if pos is None:
            return True  # All cells filled
        
        r, c = pos
        
        # Try to place a piece such that (r, c) is the center
        if can_place(r, c):
            place_piece(r, c)
            if backtrack():
                return True
            remove_piece(r, c)
        
        # Try to place a piece such that (r, c) is the top arm (center is r+1, c)
        if r + 1 < n and can_place(r+1, c):
            place_piece(r+1, c)
            if backtrack():
                return True
            remove_piece(r+1, c)
        
        # Try to place a piece such that (r, c) is the bottom arm (center is r-1, c)
        if r - 1 >= 0 and can_place(r-1, c):
            place_piece(r-1, c)
            if backtrack():
                return True
            remove_piece(r-1, c)
        
        # Try to place a piece such that (r, c) is the left arm (center is r, c+1)
        if c + 1 < n and can_place(r, c+1):
            place_piece(r, c+1)
            if backtrack():
                return True
            remove_piece(r, c+1)
        
        # Try to place a piece such that (r, c) is the right arm (center is r, c-1)
        if c - 1 >= 0 and can_place(r, c-1):
            place_piece(r, c-1)
            if backtrack():
                return True
            remove_piece(r, c-1)
        
        return False

    if backtrack():
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()