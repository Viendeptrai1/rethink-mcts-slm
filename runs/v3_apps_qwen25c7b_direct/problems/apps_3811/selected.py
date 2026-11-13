import math
from typing import List

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def find_wcd(pairs: List[List[int]]) -> int:
    min_gcd = float('inf')
    for a, b in pairs:
        current_gcd = gcd(a, b)
        if current_gcd < min_gcd:
            min_gcd = current_gcd
    
    if min_gcd == 1:
        return -1
    else:
        return min_gcd

# Read input
n = int(input())
pairs = [list(map(int, input().split())) for _ in range(n)]

# Find and print the WCD
print(find_wcd(pairs))