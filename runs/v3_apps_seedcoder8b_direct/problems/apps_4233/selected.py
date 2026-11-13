def draw_stars(n, m, grid):
    def is_star(x, y, size):
        if x - size < 0 or x + size >= n or y - size < 0 or y + size >= m:
            return False
        if grid[x][y] != '*':
            return False
        for i in range(-size, size + 1):
            if grid[x + i][y - size] != '.' or grid[x + i][y + size] != '.':
                return False
        for j in range(-size, size + 1):
            if grid[x - size][y + j] != '.' or grid[x + size][y + j] != '.':
                return False
        return True

    stars = []
    for x in range(n):
        for y in range(m):
            if grid[x][y] == '*':
                for size in range(1, min(n, m) // 2 + 1):
                    if is_star(x, y, size):
                        stars.append((x + 1, y + 1, size))
                        for i in range(-size, size + 1):
                            for j in range(-size, size + 1):
                                grid[x + i][y + j] = '.'
                        break
                else:
                    return -1

    return stars

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    grid = [data[i + 2] for i in range(n)]
    
    result = draw_stars(n, m, grid)
    
    if result == -1:
        print(-1)
    else:
        print(len(result))
        for x, y, s in result:
            print(x, y, s)

if __name__ == "__main__":
    main()