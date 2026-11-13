from collections import Counter
import math

MOD = 10**9 + 9

def count_unsorted_permutations(n, a):
    # Count the frequency of each number
    freq = Counter(a)
    
    # Calculate the total number of permutations
    total_permutations = math.factorial(n)
    
    # Calculate the number of sorted positions
    sorted_positions = 0
    current_max = -1
    for num in a:
        if num >= current_max:
            sorted_positions += 1
            current_max = num
    
    # Calculate the number of unsorted permutations
    unsorted_permutations = total_permutations // math.factorial(sorted_positions)
    
    # Adjust for repeated elements
    for count in freq.values():
        unsorted_permutations //= math.factorial(count)
    
    return unsorted_permutations % MOD

# Read input
n = int(input())
a = list(map(int, input().split()))

# Print result
print(count_unsorted_permutations(n, a))