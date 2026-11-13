import math
from sys import stdin, stdout

def min_operations_to_one(a):
    n = len(a)
    total_operations = 0
    
    while True:
        found_one = False
        for i in range(n - 1):
            if a[i] == 1 or a[i + 1] == 1:
                continue
            gcd_val = math.gcd(a[i], a[i + 1])
            if gcd_val == 1:
                a[i] = 1
                total_operations += 1
                found_one = True
                break
        if not found_one:
            return -1
        if all(x == 1 for x in a):
            return total_operations

# Read input
input = stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output result
stdout.write(str(min_operations_to_one(a)) + '\n')