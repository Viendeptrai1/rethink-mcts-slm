def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    increasing = []
    decreasing = []
    
    i = 0
    while i < n:
        j = i
        while j < n - 1 and a[j] < a[j + 1]:
            j += 1
        increasing.extend(a[i:j + 1])
        i = j + 1
    
    i = 0
    while i < n:
        j = i
        while j < n - 1 and a[j] > a[j + 1]:
            j += 1
        decreasing.extend(a[i:j + 1])
        i = j + 1
    
    if len(increasing) + len(decreasing) != n or set(increasing + decreasing) != set(a):
        print("NO")
        return
    
    print("YES")
    print(len(increasing))
    print(*increasing)
    print(len(decreasing))
    print(*decreasing[::-1])

solve()