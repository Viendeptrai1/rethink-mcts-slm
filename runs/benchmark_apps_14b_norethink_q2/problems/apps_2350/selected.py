import sys
from math import gcd

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def binomial_coefficient(n, k, p):
    if k > n:
        return 0
    num = den = 1
    for i in range(k):
        num = num * (n - i) % p
        den = den * (i + 1) % p
    return num * mod_inverse(den, p) % p

def count_unique_sums(x1, y1, x2, y2):
    p = 10**9 + 7
    n = x2 - x1 + y2 - y1
    k = x2 - x1
    return binomial_coefficient(n, k, p)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        x1 = int(data[index])
        y1 = int(data[index + 1])
        x2 = int(data[index + 2])
        y2 = int(data[index + 3])
        index += 4
        result = count_unique_sums(x1, y1, x2, y2)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()