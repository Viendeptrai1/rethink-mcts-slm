import sys
from math import gcd

def find_wcd(pairs):
    current_gcd = pairs[0][0]
    for pair in pairs[1:]:
        current_gcd = gcd(current_gcd, pair[0])
        if current_gcd <= 1:
            return -1
    return current_gcd

input = sys.stdin.read
data = input().split()
n = int(data[0])
pairs = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]

result = find_wcd(pairs)
print(result)