def draw_stars_with_asterisks(grid):
    n, m = len(grid), len(grid[0])
    
    def is_star_center(x, y, size):
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                if abs(dx) + abs(dy) == size:
                    if not (0 <= x + dx < n and 0 <= y + dy < m):
                        return False
                    if grid[x + dx][y + dy] != '*':
                        return False
        return True
    
    stars = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                if is_star_center(i, j, 1):
                    continue
                found = False
                for size in range(2, max(n, m)):
                    if is_star_center(i, j, size):
                        stars.append((i + 1, j + 1, size))
                        found = True
                        break
                if not found:
                    return -1
    
    return stars

import sys
input = sys.stdin.read
def main():
    data = input().splitlines()
    n, m = map(int, data[0].split())
    grid = data[1:n+1]
    
    result = draw_stars_with_asterisks(grid)
    
    if result == -1:
        print(result)
    else:
        print(len(result))
        for star in result:
            print(*star)

if __name__ == "__main__":
    main()