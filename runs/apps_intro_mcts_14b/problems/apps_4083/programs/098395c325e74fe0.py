import sys
from collections import Counter

def min_operations(n, k, a):
    # Count the frequency of each number in the array
    freq = Counter(a)
    
    # Sort the unique numbers in descending order
    unique_numbers = sorted(freq.keys(), reverse=True)
    
    # Initialize the minimum operations to a large number
    min_ops = float('inf')
    
    # Iterate over each unique number as a potential target value
    for target in unique_numbers:
        # Calculate the total operations needed to make at least k elements equal to target
        total_ops = 0
        count_equal_to_target = 0
        
        for num in unique_numbers:
            if num == target:
                count_equal_to_target += freq[num]
            else:
                # Calculate the number of divisions needed to make num equal to target
                divisions = 0
                current = num
                while current > target:
                    current //= 2
                    divisions += 1
                total_ops += freq[num] * divisions
        
        # If we have at least k elements equal to target, update the minimum operations
        if count_equal_to_target >= k:
            min_ops = min(min_ops, total_ops)
    
    return min_ops

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the minimum number of operations
print(min_operations(n, k, a))