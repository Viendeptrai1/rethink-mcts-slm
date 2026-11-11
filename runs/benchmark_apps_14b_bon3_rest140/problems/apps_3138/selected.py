import sys
from collections import defaultdict

def count_matching_ranges(n, numbers):
    # Dictionary to store the frequency of prefix sums
    prefix_sum_count = defaultdict(int)
    
    # Initialize variables
    total_ways = 0
    current_product = 1
    
    # Iterate through the numbers
    for i in range(n):
        # Update the current product
        current_product *= numbers[i]
        
        # Check if there exists a prefix sum that matches the current product
        if current_product in prefix_sum_count:
            total_ways += prefix_sum_count[current_product]
        
        # Update the prefix sum count
        prefix_sum_count[current_product] += 1
    
    return total_ways

# Read input
n = int(sys.stdin.readline().strip())
numbers = list(map(int, sys.stdin.readline().strip().split()))

# Calculate and print the result
print(count_matching_ranges(n, numbers))