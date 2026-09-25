import sys
from math import gcd
from functools import reduce

def lcm(a, b):
    return a * b // gcd(a, b)

def find_min_x(n, divisors):
    if n == 0:
        return -1
    if n == 1:
        return divisors[0] ** 2
    
    # Calculate LCM of all divisors
    current_lcm = reduce(lcm, divisors)
    
    # Check if current_lcm is divisible by all divisors
    for d in divisors:
        if current_lcm % d != 0:
            return -1
    
    # Check if current_lcm has exactly n+2 divisors
    def count_divisors(x):
        count = 0
        for i in range(1, int(x**0.5) + 1):
            if x % i == 0:
                count += 1
                if i != x // i:
                    count += 1
        return count
    
    if count_divisors(current_lcm) == n + 2:
        return current_lcm
    else:
        return -1

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