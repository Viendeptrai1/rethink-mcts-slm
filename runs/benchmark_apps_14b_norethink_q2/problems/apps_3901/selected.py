import sys
from math import gcd
from functools import reduce

def min_operations_to_one(n, a):
    # Calculate the GCD of the entire array
    overall_gcd = reduce(gcd, a)
    
    # If the GCD of the entire array is not 1, it's impossible to make all elements 1
    if overall_gcd != 1:
        return -1
    
    # Count the number of 1s in the array
    count_of_ones = a.count(1)
    
    # The minimum number of operations needed is the total number of elements minus the number of 1s
    return n - count_of_ones

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = min_operations_to_one(n, a)
    print(result)

if __name__ == "__main__":
    main()