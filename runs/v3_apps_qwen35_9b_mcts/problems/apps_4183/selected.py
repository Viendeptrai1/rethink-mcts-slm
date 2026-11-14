import sys
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return
    
    t_values = []
    for _ in range(n):
        t_values.append(int(next(iterator)))
    
    result = 1
    for t in t_values:
        result = lcm(result, t)
    
    print(result)

if __name__ == "__main__":
    solve()