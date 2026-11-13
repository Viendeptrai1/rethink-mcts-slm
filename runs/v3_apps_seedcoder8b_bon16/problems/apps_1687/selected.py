import math
from functools import reduce

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_divisor(arr):
    return reduce(gcd, arr)

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = find_divisor(arr)
    print(result if result != 1 else -1)

if __name__ == "__main__":
    main()