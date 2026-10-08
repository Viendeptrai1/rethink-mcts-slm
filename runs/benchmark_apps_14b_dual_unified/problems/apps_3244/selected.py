import sys

def reconstruct_ring(N, sums):
    # Create a matrix A and a vector b for the system of linear equations
    A = []
    b = []
    
    # First equation: x[0] + x[N-1] + x[1] = sums[0]
    A.append([1, 1, 1] + [0] * (N - 3))
    b.append(sums[0])
    
    # Middle equations: x[i] + x[i-1] + x[i+1] = sums[i] for i = 1 to N-2
    for i in range(1, N - 1):
        row = [0] * N
        row[i-1] = 1
        row[i] = 1
        row[i+1] = 1
        A.append(row)
        b.append(sums[i])
    
    # Last equation: x[N-2] + x[N-1] + x[0] = sums[N-1]
    A.append([0] * (N - 3) + [1, 1, 1])
    b.append(sums[N-1])
    
    # Solve the system of linear equations
    import numpy as np
    A_np = np.array(A)
    b_np = np.array(b)
    x = np.linalg.solve(A_np, b_np)
    
    # Ensure all values are non-negative
    x = np.maximum(x, 0)
    
    # Print the solution
    for value in x:
        print(int(value))

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
sums = list(map(int, data[1:]))

# Reconstruct the ring
reconstruct_ring(N, sums)