import sys
from math import gcd
from functools import reduce

def find_divisible_number(n, arr):
    # Calculate the GCD of the entire array
    common_divisor = reduce(gcd, arr)
    
    # If the GCD is greater than 1, it divides all elements
    if common_divisor > 1:
        return common_divisor
    
    # If the GCD is 1, check if 1 is in the array
    if 1 in arr:
        return 1
    
    # If no such number exists, return -1
    return -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    arr = list(map(int, data[1:n+1]))
    
    result = find_divisible_number(n, arr)
    print(result)

if __name__ == "__main__":
    main()