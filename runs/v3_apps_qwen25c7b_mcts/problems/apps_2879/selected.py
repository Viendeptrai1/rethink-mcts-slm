import sys

def find_polyomino_power(h, w, grid):
    def count_pieces():
        count = 0
        visited = [[False] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                if grid[i][j] == 'X' and not visited[i][j]:
                    count += 1
                    stack = [(i, j)]
                    while stack:
                        x, y = stack.pop()
                        if x < 0 or x >= h or y < 0 or y >= w or grid[x][y] != 'X' or visited[x][y]:
                            continue
                        visited[x][y] = True
                        stack.extend([(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]])
        return count

    def place_pieces(k):
        piece_size = count_pieces() // k
        if count_pieces() % k != 0:
            return False
        visited = [[False] * w for _ in range(h)]
        piece_num = 1
        for i in range(h):
            for j in range(w):
                if grid[i][j] == 'X' and not visited[i][j]:
                    stack = [(i, j)]
                    while stack:
                        x, y = stack.pop()
                        if x < 0 or x >= h or y < 0 or y >= w or grid[x][y] != 'X' or visited[x][y]:
                            continue
                        visited[x][y] = True
                        grid[x][y] = str(piece_num)
                        stack.extend([(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]])
                    piece_num += 1
                    if piece_num > k:
                        return False
        return True

    for k in range(2, 6):
        if place_pieces(k):
            for row in grid:
                print(''.join(row))
            return
    print("No solution")

if __name__ == "__main__":
    h, w = map(int, sys.stdin.readline().split())
    grid = [list(sys.stdin.readline().strip()) for _ in range(h)]
    find_polyomino_power(h, w, grid)