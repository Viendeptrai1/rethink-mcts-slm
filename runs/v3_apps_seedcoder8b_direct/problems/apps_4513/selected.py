def solve_anti_sudoku():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        grid = [list(data[index + i]) for i in range(9)]
        index += 9
        
        # Change at most 9 elements to make it an anti-sudoku
        changes = 0
        for i in range(9):
            for j in range(9):
                if changes >= 9:
                    break
                # Try to change the current element to make a duplicate in the row, column, or block
                original = grid[i][j]
                for new_val in map(str, range(1, 10)):
                    if new_val != original:
                        # Check row
                        if grid[i].count(new_val) < 2:
                            grid[i][j] = new_val
                            changes += 1
                            break
                        # Check column
                        if [grid[x][j] for x in range(9)].count(new_val) < 2:
                            grid[i][j] = new_val
                            changes += 1
                            break
                        # Check 3x3 block
                        block_row_start = (i // 3) * 3
                        block_col_start = (j // 3) * 3
                        block_count = sum(
                            grid[block_row_start + x][block_col_start + y] == new_val
                            for x in range(3) for y in range(3)
                        )
                        if block_count < 2:
                            grid[i][j] = new_val
                            changes += 1
                            break
                if changes >= 9:
                    break
            if changes >= 9:
                break
        
        results.append(''.join(grid[i]) for i in range(9))
    
    for result in results:
        print('\n'.join(result))