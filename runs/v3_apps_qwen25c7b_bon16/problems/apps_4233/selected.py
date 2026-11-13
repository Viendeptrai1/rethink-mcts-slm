def draw_star_grid(n, m, grid):
    def is_valid(x, y, s):
        return x - s >= 0 and x + s < n and y - s >= 0 and y + s < m
    
    def place_star(x, y, s):
        if not is_valid(x, y, s):
            return False
        for i in range(x - s, x + s + 1):
            for j in range(y - s, y + s + 1):
                if abs(i - x) + abs(j - y) > s and grid[i][j] == '*':
                    return False
        return True
    
    stars = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                found = False
                for s in range(1, min(i, j, n - i - 1, m - j - 1) + 1):
                    if place_star(i, j, s):
                        stars.append((i, j, s))
                        found = True
                        break
                if not found:
                    return -1
    
    return len(stars), stars

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    grid = [data[i+2] for i in range(n)]
    
    result = draw_star_grid(n, m, grid)
    
    if result == -1:
        print(-1)
    else:
        k, stars = result
        print(k)
        for x, y, s in stars:
            print(x + 1, y + 1, s)