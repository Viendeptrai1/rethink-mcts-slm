import sys
from math import gcd
from functools import reduce

def max_gcd_after_replacement(N, A):
    current_gcd = reduce(gcd, A)
    return max(current_gcd, max(A) // current_gcd)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = list(map(int, data[1:]))
    result = max_gcd_after_replacement(N, A)
    print(result)