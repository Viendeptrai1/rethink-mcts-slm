def solve_anti_sudoku():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        sudoku = [list(data[index + i]) for i in range(9)]
        index += 9
        
        # Make the anti-sudoku by changing at most 9 elements
        changes = 0
        for i in range(9):
            if changes == 9:
                break
            if sudoku[i][0] == sudoku[i][1]:
                sudoku[i][1] = str((int(sudoku[i][1]) % 9) + 1)
                changes += 1
            if sudoku[0][i] == sudoku[1][i]:
                sudoku[1][i] = str((int(sudoku[1][i]) % 9) + 1)
                changes += 1
        
        # Change elements in the 3x3 blocks
        for block_row in range(3):
            for block_col in range(3):
                if changes == 9:
                    break
                block = []
                for r in range(block_row * 3, (block_row + 1) * 3):
                    for c in range(block_col * 3, (block_col + 1) * 3):
                        block.append((sudoku[r][c], r, c))
                
                block.sort()
                for i in range(len(block) - 1):
                    if block[i][0] == block[i + 1][0]:
                        sudoku[block[i + 1][1]][block[i + 1][2]] = str((int(block[i + 1][0]) % 9) + 1)
                        changes += 1
                        break
        
        results.append('\n'.join(''.join(row) for row in sudoku))
    
    print('\n'.join(results))