from collections import Counter
import math

MOD = 10**9 + 9

def count_unsorted_permutations(n, a):
    # Count occurrences of each number
    count = Counter(a)
    
    # Calculate factorial of n
    fact_n = math.factorial(n)
    
    # Calculate product of factorials of counts
    prod_fact_counts = 1
    for v in count.values():
        prod_fact_counts = (prod_fact_counts * math.factorial(v)) % MOD
    
    # Number of sorted permutations
    sorted_perms = fact_n // prod_fact_counts
    
    # Total permutations
    total_perms = fact_n
    
    # Number of unsorted permutations
    unsorted_perms = (total_perms - sorted_perms + MOD) % MOD
    
    return unsorted_perms

# Read input
n = int(input())
a = list(map(int, input().split()))

# Print result
print(count_unsorted_permutations(n, a))