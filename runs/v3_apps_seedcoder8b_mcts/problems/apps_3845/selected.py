def solve():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = map(int, data.split())

    # Start with a simple grid
    h, w = 1, 1
    grid = [['#']]

    # Function to check if a position is within the grid
    def in_bounds(x, y):
        return 0 <= x < h and 0 <= y < w

    # Function to count connected components
    def count_components(color):
        visited = [[False] * w for _ in range(h)]
        def dfs(x, y):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
                    if in_bounds(nx, ny) and not visited[nx][ny] and grid[nx][ny] == color:
                        visited[nx][ny] = True
                        stack.append((nx, ny))

        count = 0
        for i in range(h):
            for j in range(w):
                if not visited[i][j] and grid[i][j] == color:
                    visited[i][j] = True
                    dfs(i, j)
                    count += 1
        return count

    # Expand the grid until we meet the conditions
    while True:
        white_components = count_components('.')
        black_components = count_components('#')

        if white_components == A and black_components == B:
            break

        # Try to expand the grid
        if white_components < A:
            # Add a new white component
            grid.append(['#'] * w)
            h += 1
        elif black_components < B:
            # Add a new black component
            for row in grid:
                row.append('#')
            w += 1

    # Print the result
    print(h, w)
    for row in grid:
        print(''.join(row))