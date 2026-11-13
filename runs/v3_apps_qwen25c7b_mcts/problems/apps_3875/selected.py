import sys
from fractions import Fraction

MOD = 1000000007

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= MOD
    return C

def matrix_pow(M, p):
    result = [[int(i == j) for j in range(len(M))] for i in range(len(M))]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mult(result, M)
        M = matrix_mult(M, M)
        p //= 2
    return result

def solve(N, A):
    dp = [Fraction(1)] * (N + 1)
    for i in range(1, N + 1):
        dp[i] = sum(dp[j] for j in range(i)) / i
    dp = [dp[i] for i in range(1, N + 1)]
    
    transition = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(min(i + 1, A[i])):
            transition[i][i - j] += 1
    
    transition = [[x * dp[i] for x in row] for i, row in enumerate(transition)]
    transition = matrix_pow(transition, N - 1)
    
    result = sum(transition[i][0] for i in range(N))
    return int(result)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = list(map(int, data[1:]))
    print(solve(N, A))