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
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:]))
    
    # Compute prefix GCDs
    prefix_gcd = [0] * n
    current = 0
    for i in range(n):
        if i == 0:
            current = a[i]
        else:
            current = gcd(current, a[i])
        prefix_gcd[i] = current
    
    # Compute suffix GCDs
    suffix_gcd = [0] * n
    current = 0
    for i in range(n - 1, -1, -1):
        if i == n - 1:
            current = a[i]
        else:
            current = gcd(current, a[i])
        suffix_gcd[i] = current
    
    max_gcd = 0
    
    # Option 1: Replace A[0]
    # The GCD will be gcd(suffix_gcd[1]) if n > 1, else 0 (but n >= 2)
    if n > 1:
        g = suffix_gcd[1]
        if g > max_gcd:
            max_gcd = g
    
    # Option 2: Replace A[i] for 1 <= i <= n-2
    # The GCD will be gcd(prefix_gcd[i-1], suffix_gcd[i+1])
    for i in range(1, n - 1):
        g = gcd(prefix_gcd[i - 1], suffix_gcd[i + 1])
        if g > max_gcd:
            max_gcd = g
    
    # Option 3: Replace A[n-1]
    # The GCD will be gcd(prefix_gcd[n-2]) if n > 1
    if n > 1:
        g = prefix_gcd[n - 2]
        if g > max_gcd:
            max_gcd = g
    
    print(max_gcd)

if __name__ == "__main__":
    solve()