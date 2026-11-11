import sys

def solve_anti_sudoku(board):
    # Find positions to change
    changes = []
    for i in range(9):
        if len(set(board[i])) == 9:  # Row has all unique numbers
            changes.append((i, board[i].index(board[i][0]), board[i][0]))
        if len(set(board[j][i] for j in range(9))) == 9:  # Column has all unique numbers
            changes.append((board[0].index(board[i][0]), i, board[i][0]))
    
    # Check 3x3 blocks
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block_numbers = set()
            for i in range(block_row, block_row + 3):
                for j in range(block_col, block_col + 3):
                    block_numbers.add(board[i][j])
            if len(block_numbers) == 9:
                # Find the first number in the block
                for i in range(block_row, block_row + 3):
                    for j in range(block_col, block_col + 3):
                        changes.append((i, j, board[i][j]))
                        break
                    else:
                        continue
                    break
    
    # Make at most 9 changes
    changes = changes[:9]
    
    # Apply changes
    for i, j, val in changes:
        board[i] = board[i][:j] + str((int(val) % 9) + 1) + board[i][j+1:]
    
    return board

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        board = [data[index + i] for i in range(9)]
        index += 9
        result = solve_anti_sudoku(board)
        results.extend(result)
    
    print('\n'.join(results))

if __name__ == "__main__":
    main()