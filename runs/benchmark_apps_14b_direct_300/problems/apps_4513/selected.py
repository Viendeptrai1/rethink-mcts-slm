import sys

def solve_anti_sudoku(board):
    changes = 0
    for i in range(9):
        if changes >= 9:
            break
        for j in range(9):
            if changes >= 9:
                break
            if board[i][j] == '1':
                board[i][j] = '2'
                changes += 1
    return board

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        board = [list(data[index + i]) for i in range(9)]
        result = solve_anti_sudoku(board)
        results.append(result)
        index += 9
    
    for result in results:
        for row in result:
            print(''.join(row))

if __name__ == "__main__":
    main()