import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    
    grid = []
    idx = 2
    for i in range(n):
        grid.append(data[idx])
        idx += 1
    
    # Create a mutable grid to mark covered cells
    covered = [['.' for _ in range(m)] for _ in range(n)]
    
    stars = []
    
    # Try to place a star at every possible center (i, j)
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '.':
                continue
            
            # Determine the maximum possible size for a star centered at (r, c)
            # The size is limited by the distance to the nearest '.' in any of the 4 directions
            # or the grid boundaries.
            
            # Check up
            up = 0
            while r - up >= 0 and grid[r - up][c] == '*':
                up += 1
            
            # Check down
            down = 0
            while r + down < n and grid[r + down][c] == '*':
                down += 1
            
            # Check left
            left = 0
            while c - left >= 0 and grid[r][c - left] == '*':
                left += 1
            
            # Check right
            right = 0
            while c + right < m and grid[r][c + right] == '*':
                right += 1
            
            # The size must be the minimum of the four arms, and must be at least 1
            max_size = min(up, down, left, right)
            
            if max_size >= 1:
                # We can place a star of size max_size here
                # However, we only need to place a star if it helps cover some '*' that hasn't been covered yet.
                # But the problem says "find any way", and we can use up to n*m stars.
                # A simple greedy approach: if we can place a star, place it with the maximum possible size.
                # This will cover the most ground.
                # Note: We don't strictly need to check if it covers uncovered stars because the problem allows overlaps.
                # But to be safe and efficient, we can just place it.
                # Actually, placing a star where there is a '*' is always valid if the arms are clear.
                # The only constraint is that the final union of stars must exactly match the input grid.
                # Since we start with an empty 'covered' grid and only add stars where the center is '*',
                # and we only add stars that are valid according to the input grid (arms are '*'),
                # the only risk is adding a star that covers a '.' which is impossible by definition of our check.
                # So we can just add all valid maximal stars.
                
                stars.append((r + 1, c + 1, max_size))
                
                # Mark the star in the covered grid
                for dr in range(-max_size, max_size + 1):
                    for dc in range(-max_size, max_size + 1):
                        if abs(dr) == max_size or abs(dc) == max_size:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < n and 0 <= nc < m:
                                covered[nr][nc] = '*'
    
    # Verify if all '*' in the original grid are covered
    possible = True
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '*' and covered[r][c] == '.':
                possible = False
                break
        if not possible:
            break
    
    if not possible:
        print("-1")
    else:
        print(len(stars))
        for r, c, s in stars:
            print(f"{r} {c} {s}")

if __name__ == "__main__":
    solve()