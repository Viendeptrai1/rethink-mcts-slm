import sys

def max_absolute_difference(n, m):
    if n == 1:
        return 0
    if n == 2:
        return m
    # Place the largest possible values at alternating positions
    # to maximize the sum of absolute differences.
    # We can place (m // 2) at one position and (m - m // 2) at the next.
    # This pattern will repeat, and we will have n elements.
    # The sum of absolute differences will be (n - 1) * (m // 2).
    return (n - 1) * (m // 2)

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