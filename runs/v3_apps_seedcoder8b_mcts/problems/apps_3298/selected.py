import sys
from math import factorial
from collections import Counter

MOD = 10**9 + 9

def count_unsorted_sequences(n, a):
    # Count the frequency of each element
    freq = Counter(a)
    
    # Calculate the total number of permutations
    total_permutations = factorial(n)
    
    # Calculate the product of factorials of frequencies
    freq_product = 1
    for count in freq.values():
        freq_product = (freq_product * factorial(count)) % MOD
    
    # Calculate the number of sorted sequences
    sorted_sequences = (total_permutations * pow(freq_product, MOD - 2, MOD)) % MOD
    
    # Calculate the number of unsorted sequences
    unsorted_sequences = (total_permutations - sorted_sequences + MOD) % MOD
    
    return unsorted_sequences

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = count_unsorted_sequences(n, a)
    print(result)

if __name__ == "__main__":
    main()