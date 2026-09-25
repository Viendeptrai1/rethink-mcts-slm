import sys
from collections import Counter

def min_operations_to_equal_numbers(n, k, a):
    # Count the frequency of each number in the array
    count = Counter(a)
    
    # Find the most frequent number and its frequency
    most_frequent_number, max_count = count.most_common(1)[0]
    
    # If the most frequent number already appears at least k times, no operations are needed
    if max_count >= k:
        return 0
    
    # Calculate the number of additional instances needed
    additional_needed = k - max_count
    
    # Initialize the minimum operations to a large number
    min_operations = float('inf')
    
    # Iterate over each unique number in the array
    for num in count:
        # Calculate the number of operations needed to transform all occurrences of num to the most frequent number
        operations = sum((num - most_frequent_number) // 2 for num in a if num != most_frequent_number)
        
        # Update the minimum operations if the current number of operations is smaller
        min_operations = min(min_operations, operations)
    
    return min_operations

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_equal_numbers(n, k, a)
print(result)