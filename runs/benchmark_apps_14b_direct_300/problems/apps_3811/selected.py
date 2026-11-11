import sys
from math import gcd
from functools import reduce

def find_wcd(pairs):
    # Calculate the GCD of all numbers in the pairs
    overall_gcd = reduce(gcd, (a for a, b in pairs))
    
    # If the overall GCD is 1, then no WCD exists
    if overall_gcd == 1:
        return -1
    
    # Otherwise, any divisor of the overall GCD greater than 1 is a valid WCD
    return overall_gcd

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    pairs = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    
    result = find_wcd(pairs)
    print(result)

if __name__ == "__main__":
    main()