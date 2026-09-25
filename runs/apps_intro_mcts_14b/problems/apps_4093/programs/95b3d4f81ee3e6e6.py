import sys

def solve(n, m):
    if n == 1:
        return 0
    if n == 2:
        return m
    if n % 2 == 0:
        return 2 * (m // n)
    else:
        return 2 * ((m // n) + (m % n))

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