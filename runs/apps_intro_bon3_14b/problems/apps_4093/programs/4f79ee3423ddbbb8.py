import sys

def solve(n, m):
    if n == 1:
        return 0
    if m == 0:
        return 0
    if n == 2:
        return m
    # We can alternate between the maximum possible values and 0
    # to maximize the sum of absolute differences.
    # The maximum value we can use is m // (n // 2)
    max_value = m // (n // 2)
    # If n is odd, we can use one more max_value
    if n % 2 == 1:
        return 2 * (max_value * (n // 2)) + max_value
    else:
        return 2 * (max_value * (n // 2))

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