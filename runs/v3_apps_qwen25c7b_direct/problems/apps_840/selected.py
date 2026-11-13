import sys

def max_cookies(n, k, a, b):
    total = sum(b)
    if total >= k:
        return 0
    
    diff = [a[i] - b[i] for i in range(n)]
    diff.sort()
    
    count = 0
    for d in diff:
        if k >= d:
            k -= d
            count += 1
        else:
            break
    
    return count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:n+2]))
    b = list(map(int, data[n+2:]))
    
    result = max_cookies(n, k, a, b)
    print(result)