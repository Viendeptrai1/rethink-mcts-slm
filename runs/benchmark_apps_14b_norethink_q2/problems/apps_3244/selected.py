import sys

def solve_luka_problem():
    import sys

    def read_int():
        return int(sys.stdin.readline().strip())

    def read_list_int():
        return list(map(int, sys.stdin.readline().strip().split()))

    N = read_int()
    sums = [read_int() for _ in range(N)]

    # Create a system of linear equations
    # Let x[i] be the i-th number in the original ring
    # We have the following equations:
    # x[i] + x[i-1] + x[i+1] = sums[i] for i in range(N)
    # We can represent this as a matrix equation Ax = b
    # Where A is an NxN matrix, x is an Nx1 vector of unknowns, and b is an Nx1 vector of sums

    # Initialize the matrix A and vector b
    A = [[0] * N for _ in range(N)]
    b = [0] * N

    for i in range(N):
        A[i][(i - 1) % N] = 1
        A[i][i] = 1
        A[i][(i + 1) % N] = 1
        b[i] = sums[i]

    # Solve the system of linear equations using Gaussian elimination
    for i in range(N):
        # Find the pivot row
        pivot_row = i
        while pivot_row < N and A[pivot_row][i] == 0:
            pivot_row += 1

        # Swap the current row with the pivot row
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            b[i], b[pivot_row] = b[pivot_row], b[i]

        # Normalize the pivot row
        pivot_value = A[i][i]
        for j in range(N):
            A[i][j] //= pivot_value
        b[i] //= pivot_value

        # Eliminate the pivot column in all other rows
        for j in range(N):
            if j != i:
                factor = A[j][i]
                for k in range(N):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]

    # Extract the solution from the last column of the augmented matrix
    solution = [b[i] for i in range(N)]

    # Print the solution
    for num in solution:
        print(num)

# Call the function to solve the problem
solve_luka_problem()