import sys

def find_min_x(n, divisors):
    # Sort the divisors to easily find the largest one
    divisors.sort()
    
    # The largest divisor in the list will be used to check if x is divisible by all divisors
    max_divisor = divisors[-1]
    
    # Check if max_divisor is divisible by all other divisors
    for d in divisors:
        if max_divisor % d != 0:
            return -1
    
    # If all divisors divide max_divisor, then max_divisor is a candidate for x
    return max_divisor

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
        divisors = list(map(int, data[index:index + n]))
        index += n
        result = find_min_x(n, divisors)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()