def draw_stars(n, m, grid):
    def is_valid_star(x, y, s):
        # Check if the star centered at (x, y) with size s is within bounds
        return 0 <= x - s < n and 0 <= x + s < n and 0 <= y - s < m and 0 <= y + s < m

    stars = []
    visited = set()

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*' and (i, j) not in visited:
                # Try to place the largest possible star centered at (i, j)
                s = min(i, n - 1 - i, j, m - 1 - j)
                while not is_valid_star(i, j, s):
                    s -= 1
                if s > 0:
                    stars.append((i + 1, j + 1, s))
                    # Mark all positions of this star as visited
                    for dx in range(-s, s + 1):
                        for dy in range(-s, s + 1):
                            if abs(dx) + abs(dy) <= s:
                                visited.add((i + dx, j + dy))
                else:
                    return "-1"

    return str(len(stars)) + "\n" + "\n".join(f"{x} {y} {s}" for x, y, s in stars)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
grid = data[2:]

# Output the result
print(draw_stars(n, m, grid))