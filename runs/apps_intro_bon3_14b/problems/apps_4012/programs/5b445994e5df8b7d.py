import sys

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def lcm(x, y):
    return x * y // gcd(x, y)

def min_operations(a, b, c):
    res = float('inf')
    best_A, best_B, best_C = None, None, None
    
    for A in range(1, a + 1):
        for B in range(A, b + 1):
            if B % A == 0:
                C = lcm(B, c)
                if C >= B:
                    ops = (A - a) + (B - b) + (C - c)
                    if ops < res:
                        res = ops
                        best_A, best_B, best_C = A, B, C
    
    return res, best_A, best_B, best_C

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