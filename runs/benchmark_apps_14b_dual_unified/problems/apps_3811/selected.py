import sys
from math import gcd

def find_wcd(pairs):
    if not pairs:
        return -1
    
    # Initialize with the GCD of the first pair
    a, b = pairs[0]
    common_divisors = {i for i in range(2, min(a, b) + 1) if a % i == 0 or b % i == 0}
    
    for a, b in pairs[1:]:
        new_common_divisors = set()
        for d in common_divisors:
            if a % d == 0 or b % d == 0:
                new_common_divisors.add(d)
        if not new_common_divisors:
            return -1
        common_divisors = new_common_divisors
    
    if not common_divisors:
        return -1
    
    return next(iter(common_divisors))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    pairs = []
    index = 1
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        pairs.append((a, b))
        index += 2
    
    result = find_wcd(pairs)
    print(result)

if __name__ == "__main__":
    main()