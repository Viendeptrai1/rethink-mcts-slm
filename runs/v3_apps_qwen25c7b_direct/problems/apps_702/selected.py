def can_tile_board(n, board):
    def dfs(x, y, visited):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == '.' and (nx, ny) not in visited:
                    stack.append((nx, ny))

    # Check if there is an odd number of connected components
    visited = set()
    components = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == '.' and (i, j) not in visited:
                dfs(i, j, visited)
                components += 1

    return components % 2 == 0

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
board = data[1:n+1]

result = "YES" if can_tile_board(n, board) else "NO"
print(result)