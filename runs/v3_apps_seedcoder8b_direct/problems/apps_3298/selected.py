import sys
from math import factorial
from collections import Counter

MOD = 10**9 + 9

def count_unsorted_permutations(n, sequence):
    # Count the frequency of each element
    freq = Counter(sequence)
    
    # Calculate the factorial of n
    total_permutations = factorial(n)
    
    # Calculate the product of factorials of frequencies
    freq_permutations = 1
    for count in freq.values():
        freq_permutations = (freq_permutations * factorial(count)) % MOD
    
    # Calculate the number of unsorted permutations
    unsorted_permutations = (total_permutations * pow(freq_permutations, MOD - 2, MOD)) % MOD
    
    return unsorted_permutations

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    sequence = list(map(int, data[1:n+1]))
    
    result = count_unsorted_permutations(n, sequence)
    print(result)

if __name__ == "__main__":
    main()