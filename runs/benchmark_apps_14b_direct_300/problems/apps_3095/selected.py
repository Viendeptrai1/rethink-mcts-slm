import sys

def is_cool_submatrix(submatrix):
    r = len(submatrix)
    s = len(submatrix[0])
    for i in range(1, r):
        for j in range(1, s):
            if submatrix[0][0] + submatrix[i][j] > submatrix[0][j] + submatrix[i][0]:
                return False
    return True

def largest_extremely_cool_submatrix(matrix):
    R = len(matrix)
    S = len(matrix[0])
    max_elements = 0
    
    for top in range(R):
        for left in range(S):
            for bottom in range(top + 1, R):
                for right in range(left + 1, S):
                    submatrix = [row[left:right+1] for row in matrix[top:bottom+1]]
                    if is_cool_submatrix(submatrix):
                        max_elements = max(max_elements, (bottom - top + 1) * (right - left + 1))
    
    return max_elements

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    S = int(data[1])
    matrix = []
    index = 2
    for _ in range(R):
        row = list(map(int, data[index:index+S]))
        matrix.append(row)
        index += S
    
    result = largest_extremely_cool_submatrix(matrix)
    print(result)