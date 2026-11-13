def find_polyomino_power(h, w, grid):
    def dfs(x, y, piece_id):
        if x < 0 or x >= h or y < 0 or y >= w or grid[x][y] == '.' or grid[x][y] != 'X':
            return True
        if grid[x][y].isdigit():
            return False
        grid[x][y] = str(piece_id)
        return all(dfs(x + dx, y + dy, piece_id) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)])

    for k in range(2, 6):
        copy_grid = [row[:] for row in grid]
        if all(dfs(i, j, 1) for i in range(h) for j in range(w)):
            return '\n'.join(''.join(row) for row in copy_grid)
    return "No solution"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    h = int(data[0])
    w = int(data[1])
    grid = data[2:]
    result = find_polyomino_power(h, w, grid)
    print(result)