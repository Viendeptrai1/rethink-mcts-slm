import sys
from math import gcd

def min_operations(a, b, c):
    # Calculate the GCD of b and c
    g = gcd(b, c)
    
    # Find the smallest A <= b that divides g
    A = b
    while A % g != 0:
        A -= 1
    
    # Find the largest B <= c that is divisible by A
    B = c
    while B % A != 0:
        B -= 1
    
    # Find the smallest C >= B that is divisible by B
    C = B
    while C < c:
        C += 1
    
    # Calculate the number of operations needed
    res = (b - A) + (c - B) + (C - c)
    
    return res, A, B, C

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        c = int(data[index + 2])
        index += 3
        
        res, A, B, C = min_operations(a, b, c)
        results.append((res, A, B, C))
    
    for res, A, B, C in results:
        print(res)
        print(A, B, C)

if __name__ == "__main__":
    main()