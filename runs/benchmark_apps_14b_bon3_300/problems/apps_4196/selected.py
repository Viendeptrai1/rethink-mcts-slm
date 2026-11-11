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
    
    # Calculate the GCD of all numbers except the second one
    gcd_excluding_second = reduce(gcd, A[2:] + [A[0]])
    
    # The maximum possible GCD after one replacement
    max_gcd = max(gcd_excluding_first, gcd_excluding_second)
    
    print(max_gcd)

if __name__ == "__main__":
    main()