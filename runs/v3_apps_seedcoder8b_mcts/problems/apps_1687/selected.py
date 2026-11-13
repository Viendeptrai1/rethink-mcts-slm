import sys
from math import gcd
from functools import reduce

def find_common_divisor(n, array):
    # Function to compute the GCD of a list of numbers
    def find_gcd_of_list(lst):
        return reduce(gcd, lst)
    
    # Check if 1 is in the array, as it is a common divisor for all positive integers
    if 1 in array:
        return 1
    
    # Find the GCD of the entire array
    overall_gcd = find_gcd_of_list(array)
    
    # If the GCD is 1, it means there is no common divisor greater than 1
    if overall_gcd == 1:
        return -1
    
    return overall_gcd

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    array = list(map(int, data[1:n+1]))
    
    result = find_common_divisor(n, array)
    print(result)

if __name__ == "__main__":
    main()