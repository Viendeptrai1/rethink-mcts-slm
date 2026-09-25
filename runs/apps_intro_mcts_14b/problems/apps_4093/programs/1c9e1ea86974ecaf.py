import sys

def max_absolute_difference(n, m):
    if n == 1:
        return 0
    # We can achieve the maximum difference by alternating between the highest and lowest possible values
    # Let's use m // 2 as the high value and m - m // 2 as the low value
    high_value = m // 2
    low_value = m - high_value
    # If n is even, we can use high_value and low_value alternately
    # If n is odd, we can use high_value one more time than low_value
    if n % 2 == 0:
        return (n // 2) * abs(high_value - low_value)
    else:
        return ((n // 2) * abs(high_value - low_value)) + abs(high_value - low_value)

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