import sys

def find_minimum_D(n, a):
    min_a = min(a)
    max_a = max(a)
    
    # If all elements are already equal, return 0
    if min_a == max_a:
        return 0
    
    # Calculate the differences between each element and the minimum element
    differences = [x - min_a for x in a]
    
    # Find the greatest common divisor (GCD) of these differences
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    
    # The GCD of all differences will be the minimum D
    min_D = differences[0]
    for diff in differences[1:]:
        min_D = gcd(min_D, diff)
    
    # Check if we can make all elements equal by adding/subtracting min_D
    for diff in differences:
        if diff % min_D != 0:
            return -1
    
    return min_D

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the minimum D
result = find_minimum_D(n, a)
print(result)