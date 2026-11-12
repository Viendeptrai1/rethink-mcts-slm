import sys
from math import gcd

def find_sequence(n, k):
    if n < k * (k + 1) // 2:
        return -1
    
    def can_form_sequence(gcd_val):
        total = 0
        current = gcd_val
        for i in range(k):
            total += current
            current += gcd_val
        return total == n
    
    max_gcd = n // k
    while max_gcd > 0:
        if can_form_sequence(max_gcd):
            return [i * max_gcd for i in range(1, k + 1)]
        max_gcd -= 1
    
    return -1

# Input reading
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Output result
result = find_sequence(n, k)
if result == -1:
    print(-1)
else:
    print(" ".join(map(str, result)))