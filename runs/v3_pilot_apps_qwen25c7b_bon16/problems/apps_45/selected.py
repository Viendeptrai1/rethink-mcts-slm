import sys
from math import gcd
from functools import reduce

def find_sequence(n, k):
    if n < k * (k + 1) // 2 or n % k != 0:
        return -1
    
    base = n // k
    seq = [base] * k
    
    # Adjust the sequence to ensure it's strictly increasing
    for i in range(k - 1, 0, -1):
        if seq[i] <= seq[i - 1]:
            seq[i] += 1
            for j in range(i):
                seq[j] = seq[j] + 1
    
    return seq

input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

result = find_sequence(n, k)
if result == -1:
    print(-1)
else:
    print(" ".join(map(str, result)))