import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # E[i] = expected steps to reach N-1 from i
    # E[N-1] = 0
    # For i != N-1: E[i] = 1 + (1/deg(i)) * sum(E[j] for j in adj[i])
    # Rearranged: E[i] - (1/deg(i)) * sum(E[j]) = 1
    # This gives a system of linear equations Ax = b

    # Variables: 0 to N-1
    # We will build matrix A of size N x N and vector b of size N
    A = [[0.0] * N for _ in range(N)]
    b = [0.0] * N

    for i in range(N):
        if i == N - 1:
            # E[N-1] = 0 => 1 * E[N-1] = 0
            A[i][i] = 1.0
            b[i] = 0.0
        else:
            deg = len(adj[i])
            # E[i] - sum(E[j]/deg) = 1
            A[i][i] = 1.0
            for j in adj[i]:
                A[i][j] -= 1.0 / deg
            b[i] = 1.0

    # Solve using Gaussian elimination with partial pivoting
    n = N
    # Forward elimination
    for col in range(n):
        # Find pivot
        pivot_row = col
        max_val = abs(A[col][col])
        for row in range(col + 1, n):
            if abs(A[row][col]) > max_val:
                max_val = abs(A[row][col])
                pivot_row = row

        # Swap rows
        A[col], A[pivot_row] = A[pivot_row], A[col]
        b[col], b[pivot_row] = b[pivot_row], b[col]

        # Normalize pivot row
        pivot_val = A[col][col]
        if abs(pivot_val) < 1e-12:
            continue  # Should not happen for this problem
        for j in range(col, n):
            A[col][j] /= pivot_val
        b[col] /= pivot_val

        # Eliminate other rows
        for row in range(n):
            if row != col:
                factor = A[row][col]
                if abs(factor) > 1e-12:
                    for j in range(col, n):
                        A[row][j] -= factor * A[col][j]
                    b[row] -= factor * b[col]

    # The solution is in b
    expected_time = b[0]
    print(f"{expected_time:.6f}")

if __name__ == "__main__":
    solve()