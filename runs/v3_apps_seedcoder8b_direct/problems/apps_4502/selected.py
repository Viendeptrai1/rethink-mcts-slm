def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    b = []
    for i in range(n):
        b.append(a[i])
        b.reverse()
    
    print(" ".join(map(str, b)))