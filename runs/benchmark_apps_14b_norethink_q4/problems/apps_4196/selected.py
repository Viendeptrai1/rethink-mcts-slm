import sys
from math import gcd
from collections import defaultdict

def max_gcd_after_move(N, A):
    # Calculate the GCD of all pairs of numbers
    max_gcd = 0
    for i in range(N):
        for j in range(i + 1, N):
            current_gcd = gcd(A[i], A[j])
            if current_gcd > max_gcd:
                max_gcd = current_gcd
    
    return max_gcd

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    result = max_gcd_after_move(N, A)
    print(result)

if __name__ == "__main__":
    main()