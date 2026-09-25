import sys

def solve(n, m):
    if n == 1:
        return 0
    if n == 2:
        return m
    if m == 0:
        return 0
    if m <= n:
        return 2 * (m - 1)
    if m >= n * (n - 1) // 2:
        return 2 * (m - n * (n - 1) // 2)
    k = (2 * m) // (n - 1)
    r = (2 * m) % (n - 1)
    return k * (n - 1) - r

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        m = int(data[index])
        index += 1
        result = solve(n, m)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()