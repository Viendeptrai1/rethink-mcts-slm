import sys
from math import gcd
from functools import reduce

def find_min_D(n, a):
    if n == 1:
        return 0
    
    # Calculate all pairwise differences
    differences = []
    for i in range(n):
        for j in range(i + 1, n):
            differences.append(abs(a[i] - a[j]))
    
    # Find the GCD of all differences
    min_D = reduce(gcd, differences)
    
    # Check if it's possible to make all elements equal
    for x in a:
        if (x - a[0]) % min_D != 0:
            return -1
    
    return min_D

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    result = find_min_D(n, a)
    print(result)

if __name__ == "__main__":
    main()