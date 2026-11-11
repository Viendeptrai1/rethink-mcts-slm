import sys
from collections import Counter
from math import factorial

MOD = 10**9 + 9

def count_entirely_unsorted_permutations(n, a):
    # Count the frequency of each element
    freq = Counter(a)
    
    # Calculate the total number of permutations
    total_permutations = factorial(n) % MOD
    
    # Calculate the number of permutations where at least one element is sorted
    sorted_permutations = 0
    
    # Iterate over each unique element and its frequency
    for value, count in freq.items():
        if count > 1:
            # Calculate the number of permutations where this element is sorted
            sorted_count = factorial(count) % MOD
            sorted_permutations += sorted_count * (total_permutations // factorial(count)) % MOD
            sorted_permutations %= MOD
    
    # Subtract the number of sorted permutations from the total permutations
    unsorted_permutations = (total_permutations - sorted_permutations) % MOD
    
    return unsorted_permutations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = count_entirely_unsorted_permutations(n, a)
    print(result)

if __name__ == "__main__":
    main()