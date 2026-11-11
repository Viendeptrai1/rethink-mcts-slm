import sys
from math import gcd
from functools import reduce

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # Calculate the GCD of all numbers except the first one
    gcd_excluding_first = reduce(gcd, A[1:])
    
    # Calculate the GCD of all numbers except the last one
    gcd_excluding_last = reduce(gcd, A[:-1])
    
    # Calculate the GCD of all numbers
    overall_gcd = reduce(gcd, A)
    
    # The maximum possible GCD after one replacement
    max_possible_gcd = max(overall_gcd, gcd_excluding_first, gcd_excluding_last)
    
    print(max_possible_gcd)

if __name__ == "__main__":
    main()