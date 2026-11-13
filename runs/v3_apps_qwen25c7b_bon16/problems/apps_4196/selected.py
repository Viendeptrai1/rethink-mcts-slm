from math import gcd
from functools import reduce
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
A = list(map(int, data[1:]))

# Find the current GCD of all numbers
current_gcd = reduce(gcd, A)

# If the current GCD is already greater than or equal to 2, return it
if current_gcd >= 2:
    print(current_gcd)
else:
    # Check if there's any number that is divisible by 2
    if any(x % 2 == 0 for x in A):
        print(2)
    else:
        # If no number is divisible by 2, check divisibility by other numbers up to 5
        for i in range(3, 6):
            if any(x % i == 0 for x in A):
                print(i)
                break
        else:
            print(1)