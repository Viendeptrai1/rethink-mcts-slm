import sys

def find_min_D(n, a):
    min_val = min(a)
    max_val = max(a)
    
    # If all elements are already equal
    if min_val == max_val:
        return 0
    
    # Calculate the differences
    differences = [x - min_val for x in a]
    
    # Find the GCD of all differences
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    
    gcd_diff = differences[0]
    for diff in differences[1:]:
        gcd_diff = gcd(gcd_diff, diff)
    
    # Check if the GCD is even
    if gcd_diff % 2 == 0:
        return gcd_diff // 2
    else:
        return -1

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the result
result = find_min_D(n, a)
print(result)