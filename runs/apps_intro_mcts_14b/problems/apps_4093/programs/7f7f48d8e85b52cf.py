import sys

def max_absolute_difference(n, m):
    if n == 1:
        return 0
    if n == 2:
        return m
    # We can alternate between the highest and lowest possible values
    # to maximize the sum of absolute differences.
    # The pattern will be [m//2, m-m//2, m//2, m-m//2, ...]
    # The number of m//2 and m-m//2 will be as balanced as possible.
    half = m // 2
    other_half = m - half
    # If n is even, we can use half and other_half equally
    if n % 2 == 0:
        return (n // 2) * abs(half - other_half)
    else:
        # If n is odd, we can use half and other_half in a way that one more element is half
        return ((n // 2) * abs(half - other_half)) + abs(half - other_half)

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