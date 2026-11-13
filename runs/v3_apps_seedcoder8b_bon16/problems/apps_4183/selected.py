import sys
from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_multiple(numbers):
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm(result, numbers[i])
    return result

def main():
    input = sys.stdin.read
    data = input().strip().split()
    
    N = int(data[0])
    T = list(map(int, data[1:N+1]))
    
    result = lcm_multiple(T)
    print(result)

if __name__ == "__main__":
    main()