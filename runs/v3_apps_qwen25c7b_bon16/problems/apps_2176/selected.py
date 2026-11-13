from collections import defaultdict
import math

MOD = 998244353

def count_good_permutations(n, s):
    # Create dictionaries to store indices of each value for the first and second elements
    index_map_a = defaultdict(list)
    index_map_b = defaultdict(list)
    
    # Populate the dictionaries with the indices of each value
    for i in range(n):
        index_map_a[s[i][0]].append(i)
        index_map_b[s[i][1]].append(i)
    
    # Initialize the result
    result = 0
    
    # Iterate over all possible values for the first element
    for a_val in set(s[i][0] for i in range(n)):
        # Get the indices where the first element equals a_val
        indices_a = index_map_a[a_val]
        
        # Iterate over all possible values for the second element
        for b_val in set(s[j][1] for j in range(n)):
            # Get the indices where the second element equals b_val
            indices_b = index_map_b[b_val]
            
            # Check if we can form a good sequence by permuting the indices of a_val and b_val
            if len(indices_a) + len(indices_b) == n:
                # Calculate the number of valid permutations
                valid_perms = math.factorial(len(indices_a)) * math.factorial(len(indices_b))
                result += valid_perms
                result %= MOD
    
    return result

# Read input
n = int(input())
s = [tuple(map(int, input().split())) for _ in range(n)]

# Output the result
print(count_good_permutations(n, s))