def contains_template(A, B):
    N = len(A)
    M = len(B)
    
    def match_at_offset(i, j):
        for x in range(M):
            for y in range(M):
                if B[x][y] == '#' and A[i + x][j + y] != '#':
                    return False
        return True
    
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            if match_at_offset(i, j):
                return "Yes"
    return "No"

import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
M = int(data[1])
A = data[2:N+2]
B = data[N+2:N+2+M]

print(contains_template(A, B))