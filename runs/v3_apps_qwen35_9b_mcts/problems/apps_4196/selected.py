import sys
import math

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200000)

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
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    if N == 2:
        # If there are only 2 numbers, we can replace one with the other (or any multiple)
        # so the GCD will be the number itself.
        print(max(A))
        return

    # Precompute prefix GCDs
    # prefix[i] = gcd(A[0], A[1], ..., A[i])
    prefix = [0] * N
    prefix[0] = A[0]
    for i in range(1, N):
        prefix[i] = gcd(prefix[i-1], A[i])

    # Precompute suffix GCDs
    # suffix[i] = gcd(A[i], A[i+1], ..., A[N-1])
    suffix = [0] * N
    suffix[N-1] = A[N-1]
    for i in range(N-2, -1, -1):
        suffix[i] = gcd(suffix[i+1], A[i])

    max_gcd = 0

    # Try removing each element A[i]
    for i in range(N):
        if i == 0:
            # GCD of remaining elements is suffix[1]
            current_gcd = suffix[1]
        elif i == N - 1:
            # GCD of remaining elements is prefix[N-2]
            current_gcd = prefix[N-2]
        else:
            # GCD of remaining elements is gcd(prefix[i-1], suffix[i+1])
            current_gcd = gcd(prefix[i-1], suffix[i+1])
        
        if current_gcd > max_gcd:
            max_gcd = current_gcd

    print(max_gcd)

if __name__ == '__main__':
    solve()