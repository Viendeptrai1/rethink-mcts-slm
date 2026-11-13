def solve_polyomino_power():
    import sys
    from itertools import product

    input = sys.stdin.read
    data = input().strip().split('\n')
    
    h, w = map(int, data[0].split())
    matrix = [list(data[i + 1]) for i in range(h)]

    def is_valid_piece(piece):
        visited = set()
        stack = [piece[0]]
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in piece:
                    stack.append((nx, ny))
        return len(visited) == len(piece)

    def extract_piece(matrix, x, y):
        piece = set()
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in piece:
                continue
            piece.add((cx, cy))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < h and 0 <= ny < w and matrix[nx][ny] == 'X':
                    stack.append((nx, ny))
        return piece

    def place_piece(matrix, piece, number):
        for x, y in piece:
            matrix[x][y] = str(number)

    def remove_piece(matrix, piece):
        for x, y in piece:
            matrix[x][y] = 'X'

    def find_pieces(matrix):
        pieces = []
        visited = set()
        for x in range(h):
            for y in range(w):
                if matrix[x][y] == 'X' and (x, y) not in visited:
                    piece = extract_piece(matrix, x, y)
                    if is_valid_piece(piece):
                        pieces.append(piece)
                        visited.update(piece)
        return pieces

    def try_powers(pieces, k):
        if not pieces:
            return True
        piece = pieces[0]
        for number in range(1, k + 1):
            for _ in range(4):  # Try all rotations
                place_piece(matrix, piece, number)
                if try_powers(pieces[1:], k):
                    return True
                remove_piece(matrix, piece)
                piece = {(y, h - 1 - x) for x, y in piece}  # Rotate 90 degrees
        return False

    pieces = find_pieces(matrix)
    for k in range(2, 6):
        if try_powers(pieces, k):
            for row in matrix:
                print(''.join(row))
            return
    print("No solution")