def can_tile_board(n, board):
    def dfs(x, y, piece_count):
        if piece_count == total_pieces:
            return True
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == '.':
                for px, py in piece:
                    if 0 <= nx + px < n and 0 <= ny + py < n and board[nx + px][ny + py] == '.':
                        board[nx + px][ny + py] = '#'
                    else:
                        break
                else:
                    if dfs(nx, ny, piece_count + 1):
                        return True
                    for px, py in piece:
                        board[nx + px][ny + py] = '.'
        return False

    piece = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
    directions = [(0, 1), (1, 0), (1, 1)]
    total_pieces = 0
    free_cells = 0

    for i in range(n):
        for j in range(n):
            if board[i][j] == '.':
                free_cells += 1
                if free_cells % 5 == 0:
                    total_pieces += 1

    if free_cells % 5 != 0:
        return "NO"

    for i in range(n):
        for j in range(n):
            if board[i][j] == '.':
                for px, py in piece:
                    if 0 <= i + px < n and 0 <= j + py < n and board[i + px][j + py] == '.':
                        board[i + px][j + py] = '#'
                    else:
                        break
                else:
                    if dfs(i, j, 1):
                        return "YES"
                    for px, py in piece:
                        board[i + px][j + py] = '.'
    return "NO"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    board = [list(data[i + 1]) for i in range(n)]
    print(can_tile_board(n, board))