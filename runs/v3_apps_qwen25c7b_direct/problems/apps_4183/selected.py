import math
from sys import stdin, stdout

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def main():
    n = int(stdin.readline())
    times = [int(stdin.readline()) for _ in range(n)]
    
    result = times[0]
    for t in times[1:]:
        result = lcm(result, t)
    
    stdout.write(str(result) + '\n')

if __name__ == "__main__":
    main()