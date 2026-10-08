def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    if n == 1:
        print("YES")
        print("0")
        return
    
    increasing = [True] * n
    decreasing = [True] * n
    
    for i in range(1, n):
        if a[i] <= a[i - 1]:
            increasing[i] = False
    
    for i in range(n - 2, -1, -1):
        if a[i] <= a[i + 1]:
            decreasing[i] = False
    
    res = []
    for i in range(n):
        if increasing[i] and decreasing[i]:
            print("NO")
            return
        elif increasing[i]:
            res.append(0)
        else:
            res.append(1)
    
    print("YES")
    print(" ".join(map(str, res)))

solve()