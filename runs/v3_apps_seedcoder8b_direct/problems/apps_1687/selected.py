def find_divisible_number(n, array):
    from math import gcd
    from functools import reduce

    # Function to compute the GCD of a list of numbers
    def find_gcd_of_list(numbers):
        return reduce(gcd, numbers)

    # Find the GCD of the entire array
    gcd_of_array = find_gcd_of_list(array)

    # Check if the GCD is a divisor of all elements in the array
    for number in array:
        if number % gcd_of_array != 0:
            return -1

    return gcd_of_array

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
array = list(map(int, data[1:n+1]))

# Find and print the result
result = find_divisible_number(n, array)
print(result)