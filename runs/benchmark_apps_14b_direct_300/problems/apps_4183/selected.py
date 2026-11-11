import sys
from math import gcd
from functools import reduce

def lcm(a, b):
    return a * b // gcd(a, b)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    times = list(map(int, data[1:]))
    
    result = reduce(lcm, times)
    print(result)

if __name__ == "__main__":
    main()