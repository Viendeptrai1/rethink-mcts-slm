def can_reorder_to_different_sums(n, a):
    from itertools import permutations

    # Calculate the total sum of the array
    total_sum = sum(a)
    
    # If the total sum is odd, it's impossible to split into two equal parts
    if total_sum % 2 != 0:
        return "-1"
    
    half_sum = total_sum // 2
    
    # Try all permutations of the array
    for perm in permutations(a):
        first_half_sum = sum(perm[:n])
        second_half_sum = sum(perm[n:])
        
        # Check if the sums of the two halves are different
        if first_half_sum != second_half_sum:
            return " ".join(map(str, perm))
    
    return "-1"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Get the result
result = can_reorder_to_different_sums(n, a)

# Print the result
print(result)