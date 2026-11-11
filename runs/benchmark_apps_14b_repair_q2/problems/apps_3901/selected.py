import sys
from math import gcd

def min_operations_to_one(n, a):
    if 1 in a:
        return n - a.count(1)
    
    # Check if GCD of all elements is 1
    overall_gcd = a[0]
    for num in a:
        overall_gcd = gcd(overall_gcd, num)
        if overall_gcd == 1:
            break
    
    if overall_gcd != 1:
        return -1
    
    # Find the minimum number of operations
    operations = 0
    for i in range(n):
        if a[i] > 1:
            operations += a[i] - 1
    
    return operations

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