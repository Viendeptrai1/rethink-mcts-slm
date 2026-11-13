import sys
import math
from functools import reduce

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def min_operations_to_one(n, array):
    if n == 1:
        return 0 if array[0] == 1 else -1
    
    gcd_value = reduce(gcd, array)
    if gcd_value != 1:
        return -1
    
    operations = 0
    ones = 0
    
    for num in array:
        if num == 1:
            ones += 1
    
    if ones > 0:
        return n - ones
    
    min_gaps = n
    for i in range(n):
        current_gcd = array[i]
        for j in range(i + 1, n):
            current_gcd = gcd(current_gcd, array[j])
            if current_gcd == 1:
                min_gaps = min(min_gaps, j - i)
                break
    
    return n + min_gaps - 1

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    array = list(map(int, data[1:n+1]))
    
    result = min_operations_to_one(n, array)
    print(result)

if __name__ == "__main__":
    main()