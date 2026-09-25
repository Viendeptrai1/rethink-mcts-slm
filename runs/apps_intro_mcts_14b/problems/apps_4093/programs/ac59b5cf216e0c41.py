import sys

def max_absolute_difference(n, m):
    if n == 1:
        return 0
    # The maximum difference can be achieved by alternating between the highest and lowest possible values
    # We can have at most n-1 differences, and each difference can be as large as possible
    # The largest possible difference is when we have (m // 2) and (m - m // 2)
    # The number of such pairs is (n // 2), and the remaining element will be 0 if n is odd
    return (n - 1) * (m // n)

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