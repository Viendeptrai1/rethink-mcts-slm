def can_tile_board(n, board):
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n

    def dfs(x, y, visited, piece):
        if len(piece) == 5:
            return True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and (nx, ny) not in visited and board[nx][ny] == '.':
                visited.add((nx, ny))
                piece.append((nx, ny))
                if dfs(nx, ny, visited, piece):
                    return True
                piece.pop()
                visited.remove((nx, ny))
        return False

    free_cells = []
    for i in range(n):
        for j in range(n):
            if board[i][j] == '.':
                free_cells.append((i, j))

    if len(free_cells) % 5 != 0:
        return "NO"

    visited = set()
    for cell in free_cells:
        if cell not in visited:
            visited.add(cell)
            piece = [cell]
            if not dfs(cell[0], cell[1], visited, piece):
                return "NO"

    return "YES"

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
board = data[1:n+1]

print(can_tile_board(n, board))