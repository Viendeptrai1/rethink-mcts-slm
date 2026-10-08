import sys
import math

def max_cookies(n, k, a, b):
    def can_bake(mid):
        total_needed = 0
        for i in range(n):
            if mid * a[i] > b[i]:
                total_needed += (mid * a[i] - b[i])
        return total_needed <= k

    low, high = 0, 10**18
    while low < high:
        mid = (low + high + 1) // 2
        if can_bake(mid):
            low = mid
        else:
            high = mid - 1
    return low

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2+n]))
    b = list(map(int, data[2+n:2+2*n]))
    
    result = max_cookies(n, k, a, b)
    print(result)

if __name__ == "__main__":
    main()