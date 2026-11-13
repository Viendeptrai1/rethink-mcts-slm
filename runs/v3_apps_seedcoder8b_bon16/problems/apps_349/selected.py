def is_possible_to_make_increasing(n, m, matrix_a, matrix_b):
    # Helper function to check if a list is strictly increasing
    def is_strictly_increasing(lst):
        return all(x < y for x, y in zip(lst, lst[1:]))

    # Check if all rows and columns in both matrices are strictly increasing
    def check_strict_increasing(matrix):
        # Check rows
        for row in matrix:
            if not is_strictly_increasing(row):
                return False
        # Check columns
        for j in range(m):
            if not is_strictly_increasing([matrix[i][j] for i in range(n)]):
                return False
        return True

    # If both matrices already satisfy the condition, print "Possible"
    if check_strict_increasing(matrix_a) and check_strict_increasing(matrix_b):
        return "Possible"

    # Try swapping pairs to check if we can achieve both matrices increasing
    for i in range(n):
        for j in range(m):
            # Swap elements at position (i, j) in matrix_a and matrix_b
            matrix_a[i][j], matrix_b[i][j] = matrix_b[i][j], matrix_a[i][j]
            
            # Check if both matrices become strictly increasing
            if check_strict_increasing(matrix_a) and check_strict_increasing(matrix_b):
                return "Possible"
            
            # Revert the swap
            matrix_a[i][j], matrix_b[i][j] = matrix_b[i][j], matrix_a[i][j]

    return "Impossible"

# Reading input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])

matrix_a = []
index = 2
for _ in range(n):
    matrix_a.append(list(map(int, data[index:index + m])))
    index += m

matrix_b = []
for _ in range(n):
    matrix_b.append(list(map(int, data[index:index + m])))
    index += m

# Output the result
print(is_possible_to_make_increasing(n, m, matrix_a, matrix_b))