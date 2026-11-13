import math
from functools import reduce

def min_operations_to_one(a):
    gcd_list = []
    
    # Calculate GCD of all pairs
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            gcd_list.append(math.gcd(a[i], a[j]))
    
    # Check if there is any pair whose GCD is 1
    if 1 in gcd_list:
        return sum(1 for num in a if num != 1)
    else:
        return -1

# Read input
n = int(input().strip())
a = list(map(int, input().strip().split()))

# Print result
print(min_operations_to_one(a))