import sys

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    S = int(data[1])
    
    matrix = []
    index = 2
    for i in range(R):
        row = list(map(int, data[index:index+S]))
        matrix.append(row)
        index += S
    
    return R, S, matrix

def is_cool_submatrix(submatrix):
    r = len(submatrix)
    s = len(submatrix[0])
    
    for i in range(1, r):
        for j in range(1, s):
            if submatrix[0][0] + submatrix[i][j] > submatrix[0][j] + submatrix[i][0]:
                return False
    return True

def find_extremely_cool_submatrix(R, S, matrix):
    max_elements = 0
    
    for start_row in range(R):
        for start_col in range(S):
            for end_row in range(start_row + 1, R):
                for end_col in range(start_col + 1, S):
                    submatrix = [row[start_col:end_col+1] for row in matrix[start_row:end_row+1]]
                    if is_cool_submatrix(submatrix):
                        max_elements = max(max_elements, (end_row - start_row + 1) * (end_col - start_col + 1))
    
    return max_elements

def main():
    R, S, matrix = read_input()
    result = find_extremely_cool_submatrix(R, S, matrix)
    print(result)

if __name__ == "__main__":
    main()