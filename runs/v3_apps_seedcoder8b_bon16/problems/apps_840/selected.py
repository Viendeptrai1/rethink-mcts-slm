def max_cookies(n, k, a, b):
    excess = [(b[i] - a[i]) for i in range(n) if b[i] > a[i]]
    excess.sort()
    
    cookies = sum(b) // sum(a)
    
    for i in range(len(excess)):
        if k >= excess[i]:
            cookies += 1
            k -= excess[i]
        else:
            break
    
    cookies += k // sum(a)
    
    return cookies

n, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

print(max_cookies(n, k, a, b))