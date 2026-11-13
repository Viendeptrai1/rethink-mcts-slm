from math import factorial
from collections import Counter

MOD = int(1e9 + 9)

def count_unsorted_sequences(n, a):
    counter = Counter(a)
    total_permutations = factorial(n)
    
    for freq in counter.values():
        total_permutations //= factorial(freq)
    
    return (total_permutations * pow(2, n, MOD)) % MOD

# Main code to read input and print output
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(count_unsorted_sequences(n, a))