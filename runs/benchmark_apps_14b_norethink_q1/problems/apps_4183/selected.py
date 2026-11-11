import sys
from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    times = list(map(int, data[1:]))
    
    result = times[0]
    for t in times[1:]:
        result = lcm(result, t)
    
    print(result)

if __name__ == "__main__":
    main()