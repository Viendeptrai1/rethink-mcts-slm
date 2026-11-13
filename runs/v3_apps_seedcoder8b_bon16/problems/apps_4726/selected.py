def solve(m, n, t):
    complexities = [
        lambda x: 1,
        lambda x: 2**x,
        lambda x: x**4,
        lambda x: x**3,
        lambda x: x**2,
        lambda x: x * math.log2(x),
        lambda x: x
    ]
    
    operations = complexities[t-1](n)
    return "AC" if operations <= m else "TLE"

if __name__ == "__main__":
    import sys
    import math
    
    m, n, t = map(int, sys.stdin.readline().split())
    print(solve(m, n, t))