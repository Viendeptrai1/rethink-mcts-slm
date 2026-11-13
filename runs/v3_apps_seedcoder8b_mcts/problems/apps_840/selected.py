def max_cookies(n, k, a, b):
    def can_make_cookies(x):
        needed_powder = 0
        for i in range(n):
            if b[i] < a[i] * x:
                needed_powder += a[i] * x - b[i]
            if needed_powder > k:
                return False
        return True

    low, high = 0, 10**9
    while low < high:
        mid = (low + high + 1) // 2
        if can_make_cookies(mid):
            low = mid
        else:
            high = mid - 1
    return low

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:n+2]))
    b = list(map(int, data[n+2:2*n+2]))
    
    result = max_cookies(n, k, a, b)
    print(result)