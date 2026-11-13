def make_anti_sudoku(sudoku):
    def has_duplicates(lst):
        return len(lst) != len(set(lst))

    def find_changes():
        changes = []
        for i in range(9):
            row = [sudoku[i][j] for j in range(9)]
            col = [sudoku[j][i] for j in range(9)]
            block = [sudoku[x][y] for x in range(i // 3 * 3, i // 3 * 3 + 3) for y in range(i % 3 * 3, i % 3 * 3 + 3)]
            if has_duplicates(row) or has_duplicates(col) or has_duplicates(block):
                continue
            for j in range(9):
                if row.count(sudoku[i][j]) == 1:
                    row[j] = str((int(row[j]) % 9) + 1)
                if col.count(sudoku[j][i]) == 1:
                    col[j] = str((int(col[j]) % 9) + 1)
                if block.count(sudoku[x][y]) == 1:
                    block[(x - i // 3 * 3) * 3 + (y - i % 3 * 3)] = str((int(block[(x - i // 3 * 3) * 3 + (y - i % 3 * 3)]) % 9) + 1)
            changes.append((i, j))
        return changes[:9]

    changes = find_changes()
    for i, j in changes:
        sudoku[i] = sudoku[i][:j] + str((int(sudoku[i][j]) % 9) + 1) + sudoku[i][j+1:]
    return sudoku

def solve(t, sudokus):
    results = []
    for _ in range(t):
        sudoku = [list(line) for line in sudokus[_].split('\n')]
        result = make_anti_sudoku(sudoku)
        results.append('\n'.join(''.join(row) for row in result))
    return '\n\n'.join(results)

# Example usage:
# t = int(input())
# sudokus = [input() for _ in range(t)]
# print(solve(t, sudokus))