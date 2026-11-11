import sys
from math import gcd
from functools import reduce

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # Calculate the GCD of all numbers
    current_gcd = reduce(gcd, A)
    
    # If the current GCD is already the maximum possible, return it
    if current_gcd > 1:
        print(current_gcd)
        return
    
    # Check if we can make the GCD at least 2 by replacing one number
    for a in A:
        if a % 2 == 0:
            print(2)
            return
    
    # If no even number is found, we can replace any number with 2
    print(2)

if __name__ == "__main__":
    main()