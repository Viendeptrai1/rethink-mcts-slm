import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def can_achieve_sum(A, B, C):
    if C >= B:
        return "NO"
    
    gcd_AB = gcd(A, B)
    
    if C % gcd_AB == 0:
        return "YES"
    else:
        return "NO"

# Read input from standard input
input_line = sys.stdin.readline().strip()
A, B, C = map(int, input_line.split())

# Determine if the objective is achievable
result = can_achieve_sum(A, B, C)

# Print the result
print(result)