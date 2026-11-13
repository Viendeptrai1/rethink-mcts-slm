import sys
from math import gcd
from functools import reduce

def max_gcd_after_replacement(N, A):
    # Calculate the current GCD of the array
    current_gcd = reduce(gcd, A)
    
    # Find all divisors of the current GCD
    divisors = set()
    for i in range(1, int(current_gcd**0.5) + 1):
        if current_gcd % i == 0:
            divisors.add(i)
            divisors.add(current_gcd // i)
    
    # Check if replacing any element with a multiple of a divisor increases the GCD
    max_gcd = current_gcd
    for divisor in divisors:
        for a in A:
            # Calculate the new GCD if we replace 'a' with 'a + divisor'
            new_gcd = gcd(current_gcd, a + divisor)
            max_gcd = max(max_gcd, new_gcd)
    
    return max_gcd

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    result = max_gcd_after_replacement(N, A)
    print(result)

if __name__ == "__main__":
    main()