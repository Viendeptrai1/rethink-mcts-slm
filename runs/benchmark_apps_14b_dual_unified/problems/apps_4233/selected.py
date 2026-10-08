def draw_stars(n, m, grid):
    def is_valid_star(x, y, s):
        # Check if a star of size s centered at (x, y) is valid
        for i in range(-s, s + 1):
            for j in range(-s, s + 1):
                if abs(i) == s or abs(j) == s:
                    nx, ny = x + i, y + j
                    if not (1 <= nx <= n and 1 <= ny <= m and grid[nx - 1][ny - 1] == '*'):
                        return False
        return True

    stars = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                found = False
                for s in range(1, min(n, m) // 2 + 1):
                    if is_valid_star(i + 1, j + 1, s):
                        stars.append((i + 1, j + 1, s))
                        found = True
                        break
                if not found:
                    return "-1"
    return str(len(stars)) + "\n" + "\n".join(f"{x} {y} {s}" for x, y, s in stars)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
grid = data[2:]

# Output result
print(draw_stars(n, m, grid))