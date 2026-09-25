import sys
from math import gcd
from functools import reduce

def lcm(a, b):
    return a * b // gcd(a, b)

def find_min_x(n, divisors):
    if n == 0:
        return -1
    if n == 1:
        return divisors[0] * 2
    current_lcm = reduce(lcm, divisors)
    for d in divisors:
        if current_lcm % d != 0:
            return -1
    return current_lcm

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