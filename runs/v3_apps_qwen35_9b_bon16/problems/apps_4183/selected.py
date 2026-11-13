import sys
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

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
    
    # We need to find the smallest time T such that T is a multiple of every T_i.
    # This is equivalent to finding the Least Common Multiple (LCM) of all T_i.
    # LCM(a, b) = (a * b) // GCD(a, b)
    
    result = t_values[0]
    for i in range(1, n):
        result = (result * t_values[i]) // gcd(result, t_values[i])
        # Given constraints and problem statement guarantee, result won't overflow
        # standard 64-bit integer logic in Python (which handles arbitrary precision anyway).
    
    print(result)

if __name__ == '__main__':
    solve()