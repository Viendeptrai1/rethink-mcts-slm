import sys
from collections import Counter

def min_operations_to_equalize(n, k, a):
    # Count the frequency of each number in the array
    count = Counter(a)
    
    # Initialize the minimum operations to a large number
    min_operations = float('inf')
    
    # Iterate over each unique number in the array
    for num in count:
        # Calculate the total number of operations needed to make all numbers equal to 'num'
        total_operations = 0
        for x in a:
            # Calculate the number of divisions needed to make x equal to num
            if x != num:
                total_operations += (x - 1).bit_length() - (num - 1).bit_length()
        
        # If the current number of operations is less than the minimum, update the minimum
        if total_operations < min_operations:
            min_operations = total_operations
    
    return min_operations

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_equalize(n, k, a)
print(result)