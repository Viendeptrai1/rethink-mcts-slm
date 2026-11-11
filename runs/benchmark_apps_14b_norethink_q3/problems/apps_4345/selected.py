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
    
    res = [-1] * n
    inc = True
    dec = True
    
    for i in range(1, n):
        if a[i] > a[i - 1]:
            if dec:
                res[i - 1] = 1
                res[i] = 0
                inc = False
            else:
                if res[i - 1] == 1:
                    print("NO")
                    return
                res[i] = 0
        elif a[i] < a[i - 1]:
            if inc:
                res[i - 1] = 0
                res[i] = 1
                dec = False
            else:
                if res[i - 1] == 0:
                    print("NO")
                    return
                res[i] = 1
        else:
            if inc and dec:
                res[i - 1] = 0
                res[i] = 1
                inc = False
                dec = False
            else:
                if res[i - 1] == 0:
                    res[i] = 1
                elif res[i - 1] == 1:
                    res[i] = 0
                else:
                    print("NO")
                    return
    
    if res[0] == -1:
        res[0] = 0
    
    print("YES")
    print(" ".join(map(str, res)))

solve()