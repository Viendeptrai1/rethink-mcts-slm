import sys
import math

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

    # Expected time E[i] to reach exit (N-1) from node i
    # E[N-1] = 0
    # For others: E[i] = 1 + (1/deg[i]) * sum(E[neighbor])
    # Rearranging: E[i] * (1 - 1/deg[i]) = 1 + (1/deg[i]) * sum_{j != i} E[j]
    # But simpler: solve linear system (I - P) * E = 1, where P is transition matrix, but only for non-exit states.
    
    # Let x[i] = expected steps from i to exit.
    # x[target] = 0
    # For i != target: x[i] = 1 + sum_{j in neighbors} (1/deg[i]) * x[j]
    # => x[i] - (1/deg[i]) * sum_{j in neighbors} x[j] = 1
    
    target = N - 1
    if target == 0:
        print("0.000000")
        return

    # Variables are 0 to N-2 (since target is fixed at 0)
    # Map original index i to variable index i if i < target
    # We'll build a system of size (N-1) x (N-1)
    
    size = N - 1
    A = [[0.0] * size for _ in range(size)]
    b = [0.0] * size

    for i in range(N):
        if i == target:
            continue
        deg = len(adj[i])
        var_idx = i  # since i < target
        
        # Coefficient for x[i] on LHS: 1 - 1/deg
        A[var_idx][var_idx] = 1.0 - 1.0 / deg
        
        # Coefficients for neighbors
        for neighbor in adj[i]:
            if neighbor == target:
                # x[target] = 0, so it contributes 0 to the sum, but the '1' on RHS remains
                continue
            else:
                neighbor_var_idx = neighbor
                A[var_idx][neighbor_var_idx] -= 1.0 / deg
        
        # RHS is 1
        b[var_idx] = 1.0

    # Solve linear system Ax = b using Gaussian elimination
    # Augmented matrix
    aug = [row[:] + [b[i]] for i, row in enumerate(A)]
    
    n = size
    for col in range(n):
        # Find pivot
        pivot_row = col
        for row in range(col + 1, n):
            if abs(aug[row][col]) > abs(aug[pivot_row][col]):
                pivot_row = row
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        
        pivot_val = aug[col][col]
        if abs(pivot_val) < 1e-12:
            # Should not happen for connected graph
            continue
        
        # Normalize pivot row
        for j in range(col, n + 1):
            aug[col][j] /= pivot_val
        
        # Eliminate other rows
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                for j in range(col, n + 1):
                    aug[row][j] -= factor * aug[col][j]
    
    # Extract solution
    x = [aug[i][n] for i in range(n)]
    
    # The answer is x[0] (since friend starts at 0)
    print(f"{x[0]:.6f}")

if __name__ == "__main__":
    solve()