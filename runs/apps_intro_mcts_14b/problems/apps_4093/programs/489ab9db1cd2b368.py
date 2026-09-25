import sys

def max_absolute_difference(n, m):
    if n == 1:
        return 0
    if n == 2:
        return m
    # Calculate the maximum possible value of the sum of absolute differences
    # We can achieve this by alternating between the highest and lowest possible values
    # Start with the highest value and alternate
    high = m // n
    low = high - 1 if m % n != 0 else high
    # The number of high values and low values
    num_high = m // n
    num_low = n - num_high
    # The maximum sum of absolute differences
    return 2 * (high - low) * min(num_high, num_low)

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