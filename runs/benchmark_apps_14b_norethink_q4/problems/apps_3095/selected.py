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

def is_cool(submatrix):
    r = len(submatrix)
    s = len(submatrix[0])
    
    for i in range(1, r):
        for j in range(1, s):
            if submatrix[0][0] + submatrix[i][j] > submatrix[0][j] + submatrix[i][0]:
                return False
    return True

def largest_extremely_cool_submatrix(R, S, matrix):
    max_size = 0
    
    for top in range(R):
        for left in range(S):
            for bottom in range(top+1, R):
                for right in range(left+1, S):
                    submatrix = [row[left:right+1] for row in matrix[top:bottom+1]]
                    if is_cool(submatrix):
                        max_size = max(max_size, (bottom - top + 1) * (right - left + 1))
    
    return max_size

def main():
    R, S, matrix = read_input()
    result = largest_extremely_cool_submatrix(R, S, matrix)
    print(result)

if __name__ == "__main__":
    main()