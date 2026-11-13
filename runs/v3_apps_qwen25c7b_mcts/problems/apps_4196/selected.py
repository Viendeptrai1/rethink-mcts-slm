import math
from sys import stdin, stdout

def max_gcd(N, A):
    min_val = min(A)
    max_val = max(A)
    gcd_val = math.gcd(min_val, max_val)
    
    # Check if we can make the minimum value a multiple of the GCD
    if min_val % gcd_val == 0:
        return gcd_val
    
    # Try to find a larger GCD by replacing the minimum value
    for i in range(1, 10**9 + 1):
        if i % gcd_val == 0 and all(a % i == 0 for a in A):
            return i
    
    return gcd_val

# Read input
N = int(stdin.readline())
A = list(map(int, stdin.readline().split()))

# Calculate and print the result
stdout.write(str(max_gcd(N, A)) + '\n')