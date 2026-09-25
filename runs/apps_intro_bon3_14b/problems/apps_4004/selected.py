import sys

def find_min_D(n, a):
    min_val = min(a)
    max_val = max(a)
    
    # If all elements are already equal, D should be 0
    if min_val == max_val:
        return 0
    
    # Calculate the differences between elements and the minimum element
    differences = [x - min_val for x in a]
    
    # Find the greatest common divisor (GCD) of these differences
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    
    D = differences[0]
    for diff in differences[1:]:
        D = gcd(D, diff)
    
    # Check if we can make all elements equal by adding/subtracting D
    for diff in differences:
        if diff % D != 0:
            return -1
    
    return D

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the minimum D
result = find_min_D(n, a)
print(result)