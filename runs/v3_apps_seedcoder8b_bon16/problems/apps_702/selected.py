def can_tile_board(n, board):
    # Directions for moving in a 5-cell piece (up, down, left, right, center)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]

    # Helper function to check if a piece can be placed at position (x, y)
    def can_place(x, y):
        cells = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == '.':
                cells.append((nx, ny))
                board[nx][ny] = '#'  # Mark as occupied
            else:
                return False  # Out of bounds or already occupied
        return True

    # Backtracking function to try to tile the board
    def backtrack(index):
        if index == n * n:
            return True
        x, y = divmod(index, n)
        if board[x][y] == '#':
            return backtrack(index + 1)
        # Try to place the piece in the current cell
        if can_place(x, y):
            if backtrack(index + 1):
                return True
            # Backtrack if placing the piece didn't lead to a solution
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                board[nx][ny] = '.'
        return False

    # Convert the board to a list of lists
    board = [list(row) for row in board]
    return "YES" if backtrack(0) else "NO"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    board = data[1:n+1]
    
    result = can_tile_board(n, board)
    print(result)