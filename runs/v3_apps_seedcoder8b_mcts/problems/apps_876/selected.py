def find_minimum_i(n, k, A0):
    # Calculate the initial sum of the array A^0
    current_sum = sum(A0)
    
    # If the initial sum is already greater than or equal to k, return 0
    if current_sum >= k:
        return 0
    
    # Initialize the step counter
    i = 1
    
    # Iterate to calculate the sum of the transformed array A^i
    while current_sum < k:
        # Calculate the next sum using the function p(x)
        current_sum = (current_sum * (n + 1)) + n
        
        # Increment the step counter
        i += 1
    
    return i

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
k = int(data[1])
A0 = list(map(int, data[2:2 + n]))

# Find and print the result
result = find_minimum_i(n, k, A0)
print(result)