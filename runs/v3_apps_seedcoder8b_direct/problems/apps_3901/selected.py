import sys
from math import gcd
from functools import reduce

def min_operations_to_one(n, a):
    # Check if there's any element that is already 1
    if 1 in a:
        return n - a.count(1)
    
    # Calculate the GCD of the entire array
    array_gcd = reduce(gcd, a)
    
    # If the GCD of the entire array is not 1, it's impossible
    if array_gcd != 1:
        return -1
    
    # If we reach here, it's possible to make all elements 1
    # The minimum number of operations is n - 1
    return n - 1

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    result = min_operations_to_one(n, a)
    print(result)

if __name__ == "__main__":
    main()