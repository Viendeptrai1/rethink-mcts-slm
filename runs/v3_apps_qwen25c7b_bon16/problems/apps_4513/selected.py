import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    
    results = []
    
    for _ in range(t):
        grid = [list(map(int, list(data[index + i]))) for i in range(9)]
        
        changes = 0
        
        # Change elements in rows
        for row in range(9):
            if len(set(grid[row])) == 9:
                for col in range(9):
                    if grid[row][col] != grid[row][(col + 1) % 9]:
                        grid[row][col] = grid[row][(col + 1) % 9]
                        changes += 1
                        break
                if changes >= 9:
                    break
        
        # Change elements in columns
        for col in range(9):
            if len(set(row[col] for row in grid)) == 9:
                for row_num in range(9):
                    if grid[(row_num + 1) % 9][col] != grid[row_num][col]:
                        grid[(row_num + 1) % 9][col] = grid[row_num][col]
                        changes += 1
                        break
                if changes >= 9:
                    break
        
        # Change elements in blocks
        for block_row in range(0, 9, 3):
            for block_col in range(0, 9, 3):
                if len({grid[r][c] for r in range(block_row, block_row + 3) for c in range(block_col, block_col + 3)}) == 9:
                    for r in range(block_row, block_row + 3):
                        for c in range(block_col, block_col + 3):
                            if grid[(r + 1) % 3 + block_row][(c + 1) % 3 + block_col] != grid[r][c]:
                                grid[(r + 1) % 3 + block_row][(c + 1) % 3 + block_col] = grid[r][c]
                                changes += 1
                                break
                        if changes >= 9:
                            break
                    if changes >= 9:
                        break
        
        results.append('\n'.join(''.join(map(str, row)) for row in grid))
        index += 9
    
    for result in results:
        print(result)
        print()

if __name__ == "__main__":
    solve()