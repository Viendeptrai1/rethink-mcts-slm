def max_chocolates(n, a, b, p, q):
    lcm_ab = a * b // gcd(a, b)
    count_ab = n // lcm_ab
    count_a_not_b = n // a - count_ab
    count_b_not_a = n // b - count_ab
    
    # Calculate chocolates if we paint all ab tiles red
    chocolates_red = count_ab * p + count_a_not_b * p + count_b_not_a * q
    
    # Calculate chocolates if we paint all ab tiles blue
    chocolates_blue = count_ab * q + count_a_not_b * p + count_b_not_a * q
    
    return max(chocolates_red, chocolates_blue)

# Function to compute the greatest common divisor (GCD) using Euclid's algorithm
def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
b = int(data[2])
p = int(data[3])
q = int(data[4])

# Output the result
print(max_chocolates(n, a, b, p, q))