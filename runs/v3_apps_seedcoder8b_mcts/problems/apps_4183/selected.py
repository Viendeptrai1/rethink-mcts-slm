import sys
from math import gcd
from functools import reduce

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_multiple(numbers):
    return reduce(lcm, numbers)

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    T = list(map(int, data[1:N+1]))
    
    result = lcm_multiple(T)
    print(result)

if __name__ == "__main__":
    main()