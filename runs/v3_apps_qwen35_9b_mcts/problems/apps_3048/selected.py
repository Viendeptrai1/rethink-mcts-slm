import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return
    
    if n <= 1:
        print(0)
        return
    
    degree = [0] * (n + 1)
    
    # Read N-1 edges
    for _ in range(n - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        degree[u] += 1
        degree[v] += 1
    
    ans = 0
    for i in range(1, n + 1):
        d = degree[i]
        if d > 1:
            ans += d * (d - 1)
    
    print(ans)

if __name__ == "__main__":
    solve()