def solve():
    A, B = map(int, input().split())
    diff = abs(B - A)
    
    if diff % 2 == 0:
        K = (A + B) // 2
        print(K)
    else:
        print("IMPOSSIBLE")

solve()