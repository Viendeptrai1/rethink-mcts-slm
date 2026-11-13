import sys
import math
from functools import reduce

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def wcd(pairs):
    def lcm(x, y):
        return x * y // gcd(x, y)
    
    def lcm_list(nums):
        return reduce(lcm, nums)
    
    candidates = set()
    
    for a, b in pairs:
        for i in range(2, int(math.sqrt(a)) + 1):
            if a % i == 0:
                candidates.add(i)
                while a % i == 0:
                    a //= i
        if a > 1:
            candidates.add(a)
        
        for i in range(2, int(math.sqrt(b)) + 1):
            if b % i == 0:
                candidates.add(i)
                while b % i == 0:
                    b //= i
        if b > 1:
            candidates.add(b)
    
    for candidate in candidates:
        if all(a % candidate == 0 or b % candidate == 0 for a, b in pairs):
            return candidate
    
    return -1

def main():
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    pairs = []
    index = 1
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        pairs.append((a, b))
        index += 2
    
    result = wcd(pairs)
    print(result)

if __name__ == "__main__":
    main()