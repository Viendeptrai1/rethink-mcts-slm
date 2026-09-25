import sys

def min_operations(a, b, c):
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    
    def lcm(x, y):
        return x * y // gcd(x, y)
    
    res = float('inf')
    best_A, best_B, best_C = -1, -1, -1
    
    for A in range(1, a + 1):
        for B in range(A, b + 1):
            if B % A == 0:
                for C in range(B, c + 1):
                    if C % B == 0:
                        operations = (A - a) + (B - b) + (c - C)
                        if operations < res:
                            res = operations
                            best_A, best_B, best_C = A, B, C
    
    return res, best_A, best_B, best_C

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
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