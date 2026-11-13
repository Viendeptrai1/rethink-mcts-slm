def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    for i in range(n-1):
        if s[i] > s[i+1]:
            print("YES")
            print(i+1, i+2)
            return
    
    print("NO")

solve()