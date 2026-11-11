def is_increasing(matrix):
    n = len(matrix)
    m = len(matrix[0])
    
    # Check rows
    for i in range(n):
        for j in range(1, m):
            if matrix[i][j] <= matrix[i][j - 1]:
                return False
    
    # Check columns
    for j in range(m):
        for i in range(1, n):
            if matrix[i][j] <= matrix[i - 1][j]:
                return False
    
    return True

def can_make_increasing(n, m, matrix1, matrix2):
    # Try to make both matrices increasing by swapping elements
    for i in range(n):
        for j in range(m):
            # Swap elements at (i, j) in both matrices
            matrix1[i][j], matrix2[i][j] = matrix2[i][j], matrix1[i][j]
            
            # Check if both matrices are now increasing
            if is_increasing(matrix1) and is_increasing(matrix2):
                return "Possible"
            
            # Swap back to original state
            matrix1[i][j], matrix2[i][j] = matrix2[i][j], matrix1[i][j]
    
    return "Impossible"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

index = 2
matrix1 = []
for _ in range(n):
    row = list(map(int, data[index:index + m]))
    matrix1.append(row)
    index += m

matrix2 = []
for _ in range(n):
    row = list(map(int, data[index:index + m]))
    matrix2.append(row)
    index += m

# Output result
print(can_make_increasing(n, m, matrix1, matrix2))