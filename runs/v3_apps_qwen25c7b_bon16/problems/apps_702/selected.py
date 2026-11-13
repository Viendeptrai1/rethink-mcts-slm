def can_tile_board(n, board):
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == '.'

    def place_piece(x, y):
        board[x][y] = 'X'
        board[x+1][y] = 'X'
        board[x][y+1] = 'X'
        board[x][y-1] = 'X'
        board[x-1][y] = 'X'

    def remove_piece(x, y):
        board[x][y] = '.'
        board[x+1][y] = '.'
        board[x][y+1] = '.'
        board[x][y-1] = '.'
        board[x-1][y] = '.'

    def dfs():
        free_cells = [(i, j) for i in range(n) for j in range(n) if board[i][j] == '.']
        if len(free_cells) % 5 != 0:
            return False

        stack = []
        visited = set()
        stack.append((free_cells[0], 0))

        while stack:
            (x, y), placed = stack[-1]
            if (x, y) in visited:
                stack.pop()
                continue

            visited.add((x, y))
            if placed == 5:
                stack.pop()
                continue

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny):
                    stack.append(((nx, ny), placed + 1))
                    break
            else:
                place_piece(x, y)
                stack.append(((x, y), 5))

        return all(board[i][j] == 'X' for i in range(n) for j in range(n) if board[i][j] != '#')

    return 'YES' if dfs() else 'NO'

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
board = data[1:n+1]
result = can_tile_board(n, board)
print(result)