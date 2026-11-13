def contains_template(N, M, A, B):
    def matches(A, B, x, y):
        for i in range(M):
            for j in range(M):
                if B[i][j] == '#' and A[x + i][y + j] != '#':
                    return False
        return True

    for i in range(N - M + 1):
        for j in range(N - M + 1):
            if matches(A, B, i, j):
                return "Yes"
    return "No"

import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])

A = data[2:N+2]
B = data[N+2:N+2+M]

print(contains_template(N, M, A, B))