import sys

def max_absolute_difference(n, m):
    if n == 1:
        return 0
    if n == 2:
        return m
    # We can alternate between the maximum possible values
    # to maximize the sum of absolute differences.
    # The pattern will be [m//2, m-m//2, m//2, m-m//2, ...]
    # If n is odd, we can add an extra 0 at the end.
    half = m // 2
    full_pairs = n // 2
    remainder = n % 2
    return 2 * half * full_pairs + remainder * half

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
        result = max_absolute_difference(n, m)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()