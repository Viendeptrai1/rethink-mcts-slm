import sys

def max_absolute_difference(n, m):
    if n == 1:
        return 0
    else:
        # The maximum sum of absolute differences is achieved by alternating between the maximum possible values
        # and 0. If n is even, we can use m/2 and m/2. If n is odd, we use (m//2) and (m//2 + m%2).
        # The number of pairs is n-1, so we can achieve a maximum difference of m.
        return m

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