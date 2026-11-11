def can_tile_board(n, board):
    # Count the number of free cells
    free_cells = sum(row.count('.') for row in board)
    
    # If the number of free cells is not divisible by 5, it's impossible to tile
    if free_cells % 5 != 0:
        return "NO"
    
    # Try to place the pieces on the board
    def dfs(x, y, placed_pieces):
        if placed_pieces == free_cells // 5:
            return True
        
        # Try placing a piece in all possible orientations
        for dx, dy in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            if x + dx + 2 < n and y + dy + 2 < n:
                if (board[x][y] == '.' and board[x+dx][y+dy] == '.' and
                    board[x+dx+1][y+dy] == '.' and board[x+dx][y+dy+1] == '.' and
                    board[x+dx+1][y+dy+1] == '.'):
                    
                    # Place the piece
                    board[x][y] = '#'
                    board[x+dx][y+dy] = '#'
                    board[x+dx+1][y+dy] = '#'
                    board[x+dx][y+dy+1] = '#'
                    board[x+dx+1][y+dy+1] = '#'
                    
                    # Try to place the next piece
                    for nx in range(n):
                        for ny in range(n):
                            if board[nx][ny] == '.':
                                if dfs(nx, ny, placed_pieces + 1):
                                    return True
                    
                    # Remove the piece (backtrack)
                    board[x][y] = '.'
                    board[x+dx][y+dy] = '.'
                    board[x+dx+1][y+dy] = '.'
                    board[x+dx][y+dy+1] = '.'
                    board[x+dx+1][y+dy+1] = '.'
        
        return False
    
    # Start DFS from the first free cell
    for i in range(n):
        for j in range(n):
            if board[i][j] == '.':
                if dfs(i, j, 0):
                    return "YES"
    
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
board = data[1:n+1]

# Output result
print(can_tile_board(n, board))