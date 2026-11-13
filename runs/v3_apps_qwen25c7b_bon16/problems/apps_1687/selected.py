import sys

def find_divisible_number():
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    # Find the GCD of the array
    from math import gcd
    result = a[0]
    for i in range(1, n):
        result = gcd(result, a[i])
    
    if result == 1:
        return -1
    else:
        return result

print(find_divisible_number())