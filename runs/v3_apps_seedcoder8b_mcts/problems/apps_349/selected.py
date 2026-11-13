def is_possible_to_make_increasing(n, m, matrix_a, matrix_b):
    # Check if a sequence is strictly increasing
    def is_strictly_increasing(seq):
        return all(x < y for x, y in zip(seq, seq[1:]))

    # Check if all rows in a matrix are strictly increasing
    def all_rows_strictly_increasing(matrix):
        return all(is_strictly_increasing(row) for row in matrix)

    # Check if all columns in a matrix are strictly increasing
    def all_columns_strictly_increasing(matrix):
        for col in range(m):
            if not is_strictly_increasing([matrix[row][col] for row in range(n)]):
                return False
        return True

    # Check if both matrices are initially strictly increasing
    if not (all_rows_strictly_increasing(matrix_a) and all_columns_strictly_increasing(matrix_a) and
            all_rows_strictly_increasing(matrix_b) and all_columns_strictly_increasing(matrix_b)):
        return "Impossible"

    # Check if we can make both matrices strictly increasing by swapping
    for i in range(n):
        for j in range(m):
            # Swap elements and check if both matrices become strictly increasing
            matrix_a[i][j], matrix_b[i][j] = matrix_b[i][j], matrix_a[i][j]

            if (all_rows_strictly_increasing(matrix_a) and all_columns_strictly_increasing(matrix_a) and
                all_rows_strictly_increasing(matrix_b) and all_columns_strictly_increasing(matrix_b)):
                return "Possible"

            # Swap back to original
            matrix_a[i][j], matrix_b[i][j] = matrix_b[i][j], matrix_a[i][j]

    return "Impossible"

# Read input
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

# Output result
print(is_possible_to_make_increasing(n, m, matrix_a, matrix_b))