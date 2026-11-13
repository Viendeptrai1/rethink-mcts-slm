def draw_stars(n, m, grid):
    def is_valid_star(x, y, s):
        if x - s < 1 or x + s > n or y - s < 1 or y + s > m:
            return False
        for i in range(max(1, x - s), min(n + 1, x + s + 1)):
            for j in range(max(1, y - s), min(m + 1, y + s + 1)):
                if (i == x or j == y) and grid[i - 1][j - 1] != '*':
                    return False
        return True

    stars = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                found = False
                for s in range(1, min(i + 1, j + 1, n - i, m - j) + 1):
                    if is_valid_star(i + 1, j + 1, s):
                        stars.append((i + 1, j + 1, s))
                        found = True
                        break
                if not found:
                    return -1
    return len(stars), stars

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
grid = data[2:]
result = draw_stars(n, m, grid)
if result == -1:
    print(-1)
else:
    print(result[0])
    for star in result[1]:
        print(*star)