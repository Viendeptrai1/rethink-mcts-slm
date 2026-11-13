def draw_stars(n, m, grid):
    def can_form_star(x, y, size):
        if x - size < 0 or x + size >= n or y - size < 0 or y + size >= m:
            return False
        for i in range(-size, size + 1):
            if grid[x + i][y] != '*' or grid[x][y + i] != '*':
                return False
        return True

    def place_star(x, y, size):
        for i in range(-size, size + 1):
            grid[x + i][y] = '.'
            grid[x][y + i] = '.'

    stars = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                max_size = min(i, n - i - 1, j, m - j - 1)
                found = False
                for size in range(max_size, 0, -1):
                    if can_form_star(i, j, size):
                        stars.append((i + 1, j + 1, size))
                        place_star(i, j, size)
                        found = True
                        break
                if not found:
                    return -1

    return stars

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    grid = [list(data[i + 2]) for i in range(n)]
    
    result = draw_stars(n, m, grid)
    
    if result == -1:
        print(-1)
    else:
        print(len(result))
        for x, y, s in result:
            print(x, y, s)

if __name__ == "__main__":
    main()