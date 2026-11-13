def solve_anti_sudoku(t, test_cases):
    def is_valid_change(grid, i, j, new_val):
        # Check row
        if grid[i].count(new_val) >= 2:
            return True
        # Check column
        if [grid[x][j] for x in range(9)].count(new_val) >= 2:
            return True
        # Check 3x3 block
        block_row_start = (i // 3) * 3
        block_col_start = (j // 3) * 3
        block_count = sum(
            grid[x][y] == new_val
            for x in range(block_row_start, block_row_start + 3)
            for y in range(block_col_start, block_col_start + 3)
        )
        if block_count >= 2:
            return True
        return False

    results = []
    for case in test_cases:
        grid = [list(row) for row in case]
        changed = 0
        for i in range(9):
            for j in range(9):
                if changed >= 9:
                    break
                for new_val in range(1, 10):
                    if str(new_val) != grid[i][j] and is_valid_change(grid, i, j, new_val):
                        grid[i][j] = str(new_val)
                        changed += 1
                        break
            if changed >= 9:
                break
        results.append("".join("".join(row) for row in grid))
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
test_cases = [data[i * 9 + 1:(i + 1) * 9 + 1] for i in range(t)]

# Solve and print output
results = solve_anti_sudoku(t, test_cases)
for result in results:
    print(result)