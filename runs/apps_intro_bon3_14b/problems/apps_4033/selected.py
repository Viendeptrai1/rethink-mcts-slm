import sys
from math import gcd

def min_perimeter(a, b):
    total = a + b
    g = gcd(a, b)
    a //= g
    b //= g
    return 2 * (a + b + g)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    result = min_perimeter(a, b)
    print(result)

if __name__ == "__main__":
    main()