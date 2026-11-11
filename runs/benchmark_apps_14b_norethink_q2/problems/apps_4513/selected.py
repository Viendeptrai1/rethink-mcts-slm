import sys

def is_valid(sudoku):
    # Check rows
    for row in sudoku:
        if len(set(row)) != 9:
            return False
    # Check columns
    for col in range(9):
        if len(set(sudoku[row][col] for row in range(9))) != 9:
            return False
    # Check blocks
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block = set()
            for i in range(3):
                for j in range(3):
                    block.add(sudoku[block_row + i][block_col + j])
            if len(block) != 9:
                return False
    return True

def make_anti_sudoku(sudoku):
    changes = 0
    for i in range(9):
        for j in range(9):
            if changes >= 9:
                break
            original_value = sudoku[i][j]
            for new_value in range(1, 10):
                if new_value == original_value:
                    continue
                sudoku[i][j] = new_value
                if is_valid(sudoku):
                    changes += 1
                    break
            else:
                sudoku[i][j] = original_value
    return sudoku

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        sudoku = [list(map(int, data[index + i])) for i in range(9)]
        index += 9
        anti_sudoku = make_anti_sudoku(sudoku)
        results.append([''.join(map(str, row)) for row in anti_sudoku])
    
    for result in results:
        for row in result:
            print(row)

if __name__ == "__main__":
    main()