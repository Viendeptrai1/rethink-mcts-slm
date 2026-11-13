def max_cookies(n, k, a, b):
    for i in range(n):
        if b[i] + k < a[i]:
            return 0
        b[i] += k
    
    min_cookies = float('inf')
    for i in range(n):
        if a[i] == 0:
            continue
        min_cookies = min(min_cookies, b[i] // a[i])
    
    return min_cookies

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:]))

print(max_cookies(n, k, a, b))