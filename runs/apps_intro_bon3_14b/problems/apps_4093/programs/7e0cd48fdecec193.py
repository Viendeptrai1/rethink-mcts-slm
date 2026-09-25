import sys

def solve(n, m):
    if n == 1:
        return 0
    if m == 0:
        return 0
    if n == 2:
        return m
    # We can alternate between 0 and m to maximize the sum of absolute differences
    # The pattern will be [m, 0, m, 0, ..., m] if n is even
    # or [m, 0, m, 0, ..., m, 0] if n is odd
    # The number of m's will be (n + 1) // 2
    # The number of 0's will be n // 2
    # The sum of absolute differences will be m * (n // 2)
    return m * (n // 2)

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