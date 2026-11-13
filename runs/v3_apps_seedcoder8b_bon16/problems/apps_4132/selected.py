import sys
from functools import reduce
from math import gcd

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # The final health of the last monster will be the GCD of all the monster's health values.
    result = reduce(gcd, A)
    
    print(result)

solve()