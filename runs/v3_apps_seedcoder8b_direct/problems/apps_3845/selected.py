def solve():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    A = int(data[0])
    B = int(data[1])

    # Start with a simple grid of size 100x100
    h, w = 100, 100
    grid = [['#' for _ in range(w)] for _ in range(h)]

    # Function to check if a cell is within the grid
    def in_bounds(x, y):
        return 0 <= x < h and 0 <= y < w

    # Directions for moving in the grid (right, down, left, up)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Function to perform DFS and mark connected components
    def dfs(x, y, color):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if grid[cx][cy] != color:
                continue
            grid[cx][cy] = color
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if in_bounds(nx, ny) and grid[nx][ny] == color:
                    stack.append((nx, ny))

    # Create A connected components of white squares
    for _ in range(A):
        x, y = 0, 0
        while grid[x][y] != '#':
            x, y = (x + 1) % h, (y + 1) % w
        dfs(x, y, '.')

    # Create B connected components of black squares
    for _ in range(B):
        x, y = 0, 0
        while grid[x][y] != '.':
            x, y = (x + 1) % h, (y + 1) % w
        dfs(x, y, '#')

    # Print the grid size
    print(h, w)
    for row in grid:
        print(''.join(row))