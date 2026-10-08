def is_cool(submatrix):
    r = len(submatrix)
    s = len(submatrix[0])
    for i in range(1, r):
        for j in range(1, s):
            if submatrix[0][0] + submatrix[i][j] > submatrix[0][j] + submatrix[i][0]:
                return False
    return True

def is_extremely_cool(matrix, r, s):
    for i in range(r):
        for j in range(s):
            for k in range(i + 2, r + 1):
                for l in range(j + 2, s + 1):
                    submatrix = [row[j:l] for row in matrix[i:k]]
                    if not is_cool(submatrix):
                        return False
    return True

def largest_extremely_cool_submatrix(matrix, R, S):
    max_elements = 0
    for r in range(2, R + 1):
        for s in range(2, S + 1):
            for i in range(R - r + 1):
                for j in range(S - s + 1):
                    submatrix = [row[j:j+s] for row in matrix[i:i+r]]
                    if is_extremely_cool(submatrix, r, s):
                        max_elements = max(max_elements, r * s)
    return max_elements

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

result = largest_extremely_cool_submatrix(matrix, R, S)
print(result)