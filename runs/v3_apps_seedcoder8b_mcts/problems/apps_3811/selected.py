import sys
from math import gcd
from functools import reduce

def find_wcd(n, pairs):
    def gcd_of_list(numbers):
        return reduce(gcd, numbers)

    def divisors(x):
        divs = set()
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0:
                divs.add(i)
                divs.add(x // i)
        divs.add(x)
        return divs

    all_divisors = set()
    for a, b in pairs:
        all_divisors.update(divisors(a))
        all_divisors.update(divisors(b))

    all_divisors = sorted(all_divisors, reverse=True)

    for divisor in all_divisors:
        if all(a % divisor == 0 or b % divisor == 0 for a, b in pairs):
            return divisor

    return -1

def main():
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

    result = find_wcd(n, pairs)
    print(result)

if __name__ == "__main__":
    main()