import sys

def solve(n, m):
    if n == 1:
        return 0
    if n % 2 == 0:
        return m
    else:
        return m - (m // (n // 2 + 1))

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
        results.append(solve(n, m))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()