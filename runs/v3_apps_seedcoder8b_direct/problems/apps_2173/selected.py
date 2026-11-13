def find_optimal_ratings():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    a.sort()
    
    b = [0] * n
    b[0] = a[0]
    
    for i in range(1, n):
        b[i] = max(a[i], b[i-1] + 1)
    
    print(" ".join(map(str, b)))