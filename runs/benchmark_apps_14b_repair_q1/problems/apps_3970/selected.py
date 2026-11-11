def largest_k_multiple_free_subset(n, k, a):
    # Sort the array to process elements in increasing order
    a.sort()
    
    # Dictionary to store groups of numbers by their remainders when divided by k
    remainder_groups = {}
    
    for num in a:
        remainder = num % k
        if remainder not in remainder_groups:
            remainder_groups[remainder] = []
        remainder_groups[remainder].append(num)
    
    # Function to get the maximum number of elements from a group
    def max_elements_from_group(group):
        # If the group has less than 2 elements, we can take all of them
        if len(group) < 2:
            return len(group)
        
        # Otherwise, we can take at most half of the elements plus one
        return (len(group) + 1) // 2
    
    # Calculate the maximum size of the k-multiple free subset
    max_size = 0
    for group in remainder_groups.values():
        max_size += max_elements_from_group(group)
    
    return max_size

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Print the result
print(largest_k_multiple_free_subset(n, k, a))