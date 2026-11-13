import math
from functools import reduce

def min_operations_to_one(n, a):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    total_gcd = reduce(gcd, a)
    if total_gcd != 1:
        return -1
    
    operations = 0
    for num in a:
        current_gcd = num
        for i in range(2, num + 1):
            if num % i == 0:
                operations += i - 1
                break
    
    return operations

# Input reading
n = int(input())
a = list(map(int, input().split()))

# Output result
print(min_operations_to_one(n, a))