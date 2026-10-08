def can_tile_board(n, board):
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == '.'

    def dfs(x, y, count):
        if count == 5:
            return True
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                board[nx][ny] = '#'
                if dfs(nx, ny, count + 1):
                    return True
                board[nx][ny] = '.'
        return False

    free_cells = sum(row.count('.') for row in board)
    if free_cells % 5 != 0:
        return "NO"

    for i in range(n):
        for j in range(n):
            if board[i][j] == '.':
                board[i][j] = '#'
                if not dfs(i, j, 1):
                    return "NO"
                board[i][j] = '.'

    return "YES"

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
board = [list(data[i + 1]) for i in range(n)]

print(can_tile_board(n, board))