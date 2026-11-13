def can_tile_board(n, board):
    # Convert board to a mutable list of lists
    board = [list(row) for row in board]
    
    # Count the number of free cells
    free_cells = sum(row.count('.') for row in board)
    
    # Check if the number of free cells is divisible by 5
    if free_cells % 5 != 0:
        return "NO"
    
    # Function to check if a position is within the board bounds
    def in_bounds(x, y):
        return 0 <= x < n and 0 <= y < n
    
    # Try to place a piece starting from a given position
    def place_piece(x, y):
        if not in_bounds(x, y) or board[x][y] != '.':
            return False
        
        # Mark the piece on the board
        directions = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny):
                board[nx][ny] = '#'
        
        return True
    
    # Try to place pieces until all free cells are covered
    while True:
        placed = False
        for i in range(n):
            for j in range(n):
                if board[i][j] == '.':
                    if place_piece(i, j):
                        placed = True
                        break
            if placed:
                break
        else:
            continue
        break
    
    # Check if all free cells are covered
    if all(cell == '#' for row in board for cell in row):
        return "YES"
    else:
        return "NO"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
board = data[1:]
result = can_tile_board(n, board)
print(result)