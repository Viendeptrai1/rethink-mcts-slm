def solve():
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    monsters_defeated = 0
    for i in range(N):
        monsters_defeated += min(A[i] + A[i+1], B[i])

    print(monsters_defeated)

solve()