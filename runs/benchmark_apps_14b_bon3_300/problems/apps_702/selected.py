def can_tile_board(n, board):
    def dfs(x, y, piece):
        if x < 0 or x >= n or y < 0 or y >= n or board[x][y] != '.':
            return False
        board[x][y] = '#'
        for dx, dy in piece:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= n or ny < 0 or ny >= n or board[nx][ny] != '.':
                for cx, cy in piece:
                    board[cx + x][cy + y] = '.'
                return False
            board[nx][ny] = '#'
        return True

    pieces = [
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (1, -1), (2, 0)]
    ]

    free_cells = [(i, j) for i in range(n) for j in range(n) if board[i][j] == '.']
    if len(free_cells) % 5 != 0:
        return "NO"

    def backtrack(index):
        if index == len(free_cells):
            return True
        x, y = free_cells[index]
        for piece in pieces:
            if dfs(x, y, piece):
                if backtrack(index + 1):
                    return True
                for dx, dy in piece:
                    board[x + dx][y + dy] = '.'
        return False

    if backtrack(0):
        return "YES"
    else:
        return "NO"

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
board = data[1:n+1]
print(can_tile_board(n, board))