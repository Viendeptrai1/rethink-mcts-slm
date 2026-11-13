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
        grid.append(next(iterator))

    # We will store the stars as a list of (r, c, size)
    stars = []

    # For each cell, if it is '*', we try to determine the maximum star size centered there.
    # A star of size s centered at (r, c) requires:
    # - (r, c) is '*'
    # - (r-k, c) is '*' for 1 <= k <= s
    # - (r+k, c) is '*' for 1 <= k <= s
    # - (r, c-k) is '*' for 1 <= k <= s
    # - (r, c+k) is '*' for 1 <= k <= s
    # And all these coordinates must be within grid bounds.

    # We iterate over every cell as a potential center.
    # If grid[r][c] is '*', we compute max possible size.
    # Then we add that star to our list.
    # Why add the maximal star? Because any star of smaller size centered here is a subset of this maximal star.
    # Since stars can overlap, adding the largest possible star at every '*' center ensures we cover all necessary '*' 
    # that are part of a valid star configuration. If a '*' is not covered by any such maximal star, then it's impossible.

    # However, we must be careful: adding a star might cover a '.' as well? No, because we only add a star if all required cells are '*'.
    # So the star we add is valid and only covers '*' cells (and the center).
    # The union of these stars must exactly match the grid's '*' positions.
    # If there is a '*' in the grid that is not covered by any of our added stars, then output -1.

    # Algorithm:
    # 1. Initialize a result grid (or boolean mask) of size n x m with False.
    # 2. For each cell (r, c) where grid[r][c] == '*':
    #    a. Determine max_size.
    #    b. If max_size > 0, add star (r, c, max_size) and mark all its cells as covered in the mask.
    # 3. After checking all centers, compare the mask with the original grid.
    #    If any cell is '*' in original but False in mask, return -1.
    #    Otherwise, output the number of stars and their parameters.

    result_mask = [[False] * m for _ in range(n)]
    stars_list = []

    for r in range(n):
        for c in range(m):
            if grid[r][c] == '*':
                # Calculate max size for center (r, c)
                # Check up, down, left, right
                up = 0
                while r - up - 1 >= 0 and grid[r - up - 1][c] == '*':
                    up += 1
                
                down = 0
                while r + down + 1 < n and grid[r + down + 1][c] == '*':
                    down += 1
                
                left = 0
                while c - left - 1 >= 0 and grid[r][c - left - 1] == '*':
                    left += 1
                
                right = 0
                while c + right + 1 < m and grid[r][c + right + 1] == '*':
                    right += 1
                
                size = min(up, down, left, right)
                
                if size > 0:
                    # Add this star
                    stars_list.append((r + 1, c + 1, size)) # 1-based indexing for output
                    # Mark covered cells
                    # Center
                    result_mask[r][c] = True
                    # Up
                    for k in range(1, size + 1):
                        result_mask[r - k][c] = True
                    # Down
                    for k in range(1, size + 1):
                        result_mask[r + k][c] = True
                    # Left
                    for k in range(1, size + 1):
                        result_mask[r][c - k] = True
                    # Right
                    for k in range(1, size + 1):
                        result_mask[r][c + k] = True

    # Verify coverage
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '*' and not result_mask[r][c]:
                print("-1")
                return

    # Output result
    print(len(stars_list))
    for r, c, s in stars_list:
        print(f"{r} {c} {s}")

if __name__ == "__main__":
    solve()