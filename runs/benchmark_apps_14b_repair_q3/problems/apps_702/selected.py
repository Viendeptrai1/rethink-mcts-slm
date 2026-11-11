def can_tile_board(n, board):
    def dfs(x, y, piece):
        if x < 0 or x >= n or y < 0 or y >= n or board[x][y] != '.':
            return False
        board[x][y] = '#'
        if piece == 4:
            return True
        dx, dy = directions[piece]
        return dfs(x + dx, y + dy, (piece + 1) % 4)
    
    def place_piece(x, y):
        if not dfs(x, y, 0):
            return False
        if not dfs(x, y, 1):
            return False
        if not dfs(x, y, 2):
            return False
        if not dfs(x, y, 3):
            return False
        return True
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    free_cells = sum(row.count('.') for row in board)
    
    if free_cells % 5 != 0:
        return "NO"
    
    for i in range(n):
        for j in range(n):
            if board[i][j] == '.':
                if not place_piece(i, j):
                    return "NO"
    
    return "YES"

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
board = [list(row) for row in data[1:n+1]]  # Convert each row to a list
print(can_tile_board(n, board))