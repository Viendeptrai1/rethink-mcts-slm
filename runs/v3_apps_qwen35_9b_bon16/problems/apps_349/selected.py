import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        
        matrix_a = []
        for _ in range(n):
            row = []
            for _ in range(m):
                row.append(int(next(iterator)))
            matrix_a.append(row)
            
        matrix_b = []
        for _ in range(n):
            row = []
            for _ in range(m):
                row.append(int(next(iterator)))
            matrix_b.append(row)
    except StopIteration:
        return

    # At each position (i, j), we have two numbers: matrix_a[i][j] and matrix_b[i][j]
    # To maximize our chances of making both matrices strictly increasing, we should ensure that:
    # min_val = min(matrix_a[i][j], matrix_b[i][j])
    # max_val = max(matrix_a[i][j], matrix_b[i][j])
    # We assign min_val to the "smaller" matrix at that position and max_val to the "larger" matrix.
    # This is because if we can form two increasing sequences using the set {min, max} at each position,
    # then assigning the smaller to one matrix and larger to the other is the optimal strategy to satisfy
    # the row and column constraints for both. Specifically, if matrix_A[i][j] < matrix_B[i][j] initially,
    # we keep it as is (or swap if needed to maintain the invariant that matrix_A[i][j] <= matrix_B[i][j]).
    # Actually, the strategy is: at every cell, force the first matrix to have the minimum of the two values
    # and the second matrix to have the maximum. If this configuration allows both to be strictly increasing,
    # then it is possible. If not, then no other configuration can work because any other configuration would
    # involve swapping some elements to make one matrix larger and the other smaller, which tightens the constraints.
    
    for i in range(n):
        for j in range(m):
            if matrix_a[i][j] > matrix_b[i][j]:
                matrix_a[i][j], matrix_b[i][j] = matrix_b[i][j], matrix_a[i][j]
    
    # Now check if matrix_a is strictly increasing (rows and columns)
    # Check rows for matrix_a
    for i in range(n):
        for j in range(1, m):
            if matrix_a[i][j] <= matrix_a[i][j-1]:
                print("Impossible")
                return
    
    # Check columns for matrix_a
    for j in range(m):
        for i in range(1, n):
            if matrix_a[i][j] <= matrix_a[i-1][j]:
                print("Impossible")
                return

    # Check rows for matrix_b
    for i in range(n):
        for j in range(1, m):
            if matrix_b[i][j] <= matrix_b[i][j-1]:
                print("Impossible")
                return
    
    # Check columns for matrix_b
    for j in range(m):
        for i in range(1, n):
            if matrix_b[i][j] <= matrix_b[i-1][j]:
                print("Impossible")
                return

    print("Possible")

if __name__ == "__main__":
    solve()