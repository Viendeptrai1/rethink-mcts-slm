import sys
import random

def is_valid_anti_sudoku(grid):
    # Check rows
    for row in grid:
        if len(set(row)) == 9:
            return False
    
    # Check columns
    for col in range(9):
        if len(set(grid[row][col] for row in range(9))) == 9:
            return False
    
    # Check 3x3 blocks
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            block = set()
            for row in range(start_row, start_row + 3):
                for col in range(start_col, start_col + 3):
                    block.add(grid[row][col])
            if len(block) == 9:
                return False
    
    return True

def make_anti_sudoku(grid):
    changes = 0
    while changes < 9:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        new_value = random.randint(1, 9)
        if grid[row][col] != new_value:
            grid[row][col] = new_value
            changes += 1
            if is_valid_anti_sudoku(grid):
                break
    return grid

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        grid = [list(map(int, data[index + i])) for i in range(9)]
        index += 9
        anti_sudoku_grid = make_anti_sudoku(grid)
        results.append([''.join(map(str, row)) for row in anti_sudoku_grid])
    
    for result in results:
        for row in result:
            print(row)

if __name__ == "__main__":
    main()