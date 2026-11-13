def can_tile_board(n, board):
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n

    def can_place_piece(x, y):
        # Check if the piece can be placed at (x, y)
        piece = [
            (x, y), (x, y+1), (x, y+2),
            (x+1, y), (x+1, y+1)
        ]
        for px, py in piece:
            if not is_valid(px, py) or board[px][py] == '#':
                return False
        return True

    def place_piece(x, y):
        # Place the piece at (x, y)
        piece = [
            (x, y), (x, y+1), (x, y+2),
            (x+1, y), (x+1, y+1)
        ]
        for px, py in piece:
            board[px][py] = '#'

    def remove_piece(x, y):
        # Remove the piece from (x, y)
        piece = [
            (x, y), (x, y+1), (x, y+2),
            (x+1, y), (x+1, y+1)
        ]
        for px, py in piece:
            board[px][py] = '.'

    def backtrack(x, y):
        if y == n:
            x, y = x + 1, 0
        if x == n:
            return True
        if board[x][y] == '#':
            return backtrack(x, y + 1)
        if can_place_piece(x, y):
            place_piece(x, y)
            if backtrack(x, y + 1):
                return True
            remove_piece(x, y)
        return backtrack(x, y + 1)

    return "YES" if backtrack(0, 0) else "NO"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    board = data[1:n+1]
    print(can_tile_board(n, board))