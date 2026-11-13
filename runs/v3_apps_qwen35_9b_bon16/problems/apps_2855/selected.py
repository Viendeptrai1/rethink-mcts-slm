import sys
import random
from functools import lru_cache

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

    # Degree of each node
    degree = [len(adj[i]) for i in range(N)]

    # Let E[i] be the expected additional steps from node i to reach node N-1.
    # We want E[0].
    # For node i != N-1: E[i] = 1 + sum(E[j] / degree[i]) for j in neighbors of i
    # Rearranging: E[i] * (1 - sum(1/degree[i] for j in neighbors)) = 1 + sum(E[j]/degree[i])
    # But note: sum(1/degree[i]) over neighbors is exactly (degree[i] * (1/degree[i])) = 1? No.
    # Actually, the equation is:
    # E[i] = 1 + (1/deg[i]) * sum(E[j] for j in neighbors)
    # => deg[i]*E[i] = deg[i] + sum(E[j])
    # => deg[i]*E[i] - sum(E[j]) = deg[i]
    # For i = N-1, E[N-1] = 0.

    # We have N-1 variables (0 to N-2) with N-1 linear equations.
    # Let's set up a system Ax = b where x = [E[0], E[1], ..., E[N-2]]
    # Coefficients:
    # For each i in 0..N-2:
    #   coeff[i][i] = degree[i]
    #   for each neighbor j of i:
    #      if j != N-1:
    #          coeff[i][j] -= 1
    #      else:
    #          # neighbor is target, its E is 0, so no variable term, but contributes to constant?
    #          # The equation is: degree[i]*E[i] - sum_{j!=N-1} E[j] = degree[i] + sum_{j=N-1} (0) ... wait.
    #          # Original: E[i] = 1 + (1/d) * (sum_{j!=N-1} E[j] + E[N-1])
    #          # E[N-1] = 0.
    #          # => d*E[i] - sum_{j!=N-1} E[j] = d
    #          # So RHS is d.
    #   RHS[i] = degree[i]

    # Build matrix
    size = N - 1  # variables 0 to N-2
    if size == 0:
        # Only exit node? But N>=2, so this case won't happen unless N=1 which is not allowed.
        print(f"{0.0:.6f}")
        return

    A = [[0.0] * size for _ in range(size)]
    B = [0.0] * size

    for i in range(size):
        # Node index i corresponds to variable i
        node = i
        d = degree[node]
        A[i][i] = d
        for neighbor in adj[node]:
            if neighbor == N - 1:
                # Target, E[neighbor] = 0, so no variable on LHS.
                # But the constant term comes from the "1" in the expectation formula multiplied by d?
                # Equation: d*E[i] - sum(E[j] for j in neighbors, j!=N-1) = d * 1
                pass
            else:
                # Variable for neighbor
                if neighbor < size:
                    A[i][neighbor] -= 1.0
                # else neighbor is N-1, handled above

        B[i] = d

    # Solve linear system using Gaussian elimination
    # Augmented matrix
    aug = [row[:] + [B[i]] for i, row in enumerate(A)]

    pivot_row = 0
    for col in range(size):
        # Find pivot
        max_row = pivot_row
        for r in range(pivot_row + 1, size):
            if abs(aug[r][col]) > abs(aug[max_row][col]):
                max_row = r
        aug[pivot_row], aug[max_row] = aug[max_row], aug[pivot_row]

        if abs(aug[pivot_row][col]) < 1e-9:
            # Should not happen for connected graph
            continue

        # Normalize pivot row
        div = aug[pivot_row][col]
        for c in range(col, size + 1):
            aug[pivot_row][c] /= div

        # Eliminate other rows
        for r in range(size):
            if r != pivot_row:
                factor = aug[r][col]
                if abs(factor) > 1e-9:
                    for c in range(col, size + 1):
                        aug[r][c] -= factor * aug[pivot_row][c]

        pivot_row += 1

    # Extract solution
    E = [aug[i][size] for i in range(size)]
    # E[i] corresponds to node i
    ans = E[0]
    print(f"{ans:.6f}")

if __name__ == "__main__":
    solve()