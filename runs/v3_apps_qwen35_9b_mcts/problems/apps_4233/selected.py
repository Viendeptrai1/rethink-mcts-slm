import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    grid = []
    for _ in range(n):
        try:
            row = next(iterator)
            grid.append(row)
        except StopIteration:
            break

    if len(grid) != n:
        print("-1")
        return

    # Check if all rows have length m
    for row in grid:
        if len(row) != m:
            print("-1")
            return

    # Identify all possible stars
    stars = []
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '*':
                # Try to find the largest possible size for a star centered at (r, c)
                size = 0
                # Check up, down, left, right
                # We need at least size 1, so check distance 1 first
                can_extend = True
                while True:
                    size += 1
                    # Check boundaries
                    if r - size < 0 or r + size >= n or c - size < 0 or c + size >= m:
                        can_extend = False
                        break
                    # Check content
                    if grid[r - size][c] != '*' or grid[r + size][c] != '*' or \
                       grid[r][c - size] != '*' or grid[r][c + size] != '*':
                        can_extend = False
                        break
                    if size >= 1:
                        # If we reached size 1 and it's valid, we can stop extending if we want minimal,
                        # but the problem says "any way", so we can just take the max valid size.
                        # Actually, we need to check if size 1 is valid first.
                        pass
                
                # Re-evaluate properly: find max size starting from 1
                max_s = 0
                if grid[r][c] == '*':
                    s = 1
                    while True:
                        if r - s < 0 or r + s >= n or c - s < 0 or c + s >= m:
                            break
                        if grid[r - s][c] != '*' or grid[r + s][c] != '*' or \
                           grid[r][c - s] != '*' or grid[r][c + s] != '*':
                            break
                        max_s = s
                        s += 1
                
                if max_s > 0:
                    stars.append((r + 1, c + 1, max_s))

    # Create a grid of dots to simulate the result
    result = [['.' for _ in range(m)] for _ in range(n)]

    # Apply all stars
    for r, c, s in stars:
        # Center
        result[r-1][c-1] = '*'
        # Rays
        for k in range(1, s + 1):
            result[r-1-k][c-1] = '*'
            result[r-1+k][c-1] = '*'
            result[r-1][c-1-k] = '*'
            result[r-1][c-1+k] = '*'

    # Verify
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '*':
                if result[r][c] != '*':
                    print("-1")
                    return
            else:
                if result[r][c] == '*':
                    print("-1")
                    return

    print(len(stars))
    for r, c, s in stars:
        print(f"{r} {c} {s}")

if __name__ == "__main__":
    solve()