import sys

def solve():
    N, M = map(int, input().split())
    A = [input().strip() for _ in range(N)]
    B = [input().strip() for _ in range(M)]

    def match(i, j):
        for x in range(M):
            for y in range(M):
                if A[i+x][j+y] != B[x][y]:
                    return False
        return True

    for i in range(N - M + 1):
        for j in range(N - M + 1):
            if match(i, j):
                print("Yes")
                return

    print("No")

solve()