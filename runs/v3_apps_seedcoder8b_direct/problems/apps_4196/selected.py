import sys
from math import gcd
from functools import reduce

def max_gcd_after_replacement():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # Calculate the current GCD of the array
    current_gcd = reduce(gcd, A)
    
    # Check if replacing any single element can increase the GCD
    max_gcd = current_gcd
    
    for i in range(N):
        # Try replacing A[i] with every number from 1 to 10^9
        # But we only need to check numbers that are divisors of the current GCD
        # because replacing with a number not dividing the GCD won't help.
        
        # Check divisors of the current GCD
        for divisor in range(1, int(current_gcd**0.5) + 1):
            if current_gcd % divisor == 0:
                # Check both divisor and its pair
                for candidate in (divisor, current_gcd // divisor):
                    if candidate < 1 or candidate > 10**9:
                        continue
                    
                    # Calculate the new GCD if we replace A[i] with candidate
                    new_gcd = reduce(gcd, A[:i] + [candidate] + A[i+1:])
                    max_gcd = max(max_gcd, new_gcd)
        
        # Also consider replacing with numbers that are not divisors of the current GCD
        # but are factors of A[i]
        for factor in range(1, int(A[i]**0.5) + 1):
            if A[i] % factor == 0:
                for candidate in (factor, A[i] // factor):
                    if candidate < 1 or candidate > 10**9:
                        continue
                    
                    # Calculate the new GCD if we replace A[i] with candidate
                    new_gcd = reduce(gcd, A[:i] + [candidate] + A[i+1:])
                    max_gcd = max(max_gcd, new_gcd)
    
    print(max_gcd)